import uuid
from datetime import timedelta, datetime
from typing import Optional
import time

import jwt
import secrets

from debugpy.adapter import access_token
from fastapi import Request, Response, status, HTTPException, FastAPI
from fastapi.openapi.models import HTTPBase as HTTPBaseModel
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security.base import SecurityBase
from fastapi.security.utils import get_authorization_scheme_param

from app.models import User
from app.schemas.auth import TokenResponse, LoginRequest
from app.utils.security import get_password_hash, verify_password, generate_token
from app.backend.config import settings
from app.services.user import user_service
from app.ext import NotFoundException, BadRequestException

ALGORITHM = "HS256"


class ResponseMessages:
    """Error strings for different circumstances."""

    CANT_GENERATE_JWT = "Unable to generate the JWT"
    CANT_GENERATE_REFRESH = "Unable to generate the Refresh Token"
    CANT_GENERATE_VERIFY = "Unable to generate the Verification Token"
    INVALID_TOKEN = "That token is Invalid"
    EXPIRED_TOKEN = "That token has Expired"
    VERIFICATION_SUCCESS = "User succesfully Verified"
    USER_NOT_FOUND = "User not Found"
    ALREADY_VALIDATED = "You are already validated"
    INCORRECT_CREDENTIALS = "Incorrect username or password"


def encode(self, data: dict):
    encode = jwt.encode(data, settings.secret_key, algorithm=ALGORITHM)
    return encode


def decode(self, token):
    decode = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
    return decode


class Token:
    def __init__(self, user: Optional[User] = None, token: Optional[str] = None):
        self.user = user
        self.token = token

    def claim_token(self):
        if self.user and self.token is None:
            data = {
                'sub': self.user.username,
                'iat': int(time.time()),
                'jti': generate_token(12),
                'nbf': int(time.time()),
            }
        else:
            data = self.decode(self.token)
        return data

    def access_token(self):
        claim = self.claim_token().copy()
        claim.update({
            'exp': datetime.utcnow() + settings.access_token_lifetime,
        })
        return self.encode(claim)

    def refresh_token(self):
        claim = self.claim_token().copy()
        claim.update({
            'exp': datetime.utcnow() + settings.refresh_token_lifetime,
        })
        return self.encode(claim)

    def encode(self, data: dict):
        encode = jwt.encode(data, settings.secret_key, algorithm=ALGORITHM)
        return encode

    def decode(self, token):
        decode = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        return decode

    def create_token(self) -> TokenResponse:
        token = TokenResponse(
            access_token=self.access_token(),
            refresh_token=self.refresh_token())
        return token

    def verify(self):
        return True


class AuthService:

    async def login(self, body: LoginRequest) -> TokenResponse:
        clause = User.username == body.username if body.username \
            else User.phone == body.phone
        user = await user_service.get_user(clause)
        credential_exception = BadRequestException(
            detail=ResponseMessages.INCORRECT_CREDENTIALS,
        )
        if not user:
            raise credential_exception
        if not verify_password(body.password, user.hashed_password):
            raise credential_exception
        # TODO: create (access, refresh) token
        token = Token(user)
        return token.create_token()

    def refresh_token(self, token: str) -> TokenResponse:
        ...


auth_service = AuthService()


class JwtAuthentication(SecurityBase):
    '''
    :: get user with token  and add request.scope['user']
    :return credentionals
    '''

    def __init__(self,
                 *,
                 scheme: str,
                 scheme_name: Optional[str] = None,
                 description: Optional[str] = None,
                 auto_error: bool = True,
                 ):
        self.model = HTTPBaseModel(scheme=scheme, description=description)
        self.scheme_name = scheme_name
        self.auto_error = auto_error
        self.token = Token()

    async def __call__(self, request: Request, response: Response) -> Optional[HTTPAuthorizationCredentials]:
        authorization = request.cookies.get("access_token") or request.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)
        credentials_exception = BadRequestException(
            detail=ResponseMessages.INCORRECT_CREDENTIALS,
        )

        if not (authorization and scheme and credentials):
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            else:
                return None
        try:
            payload = self.token.decode(credentials)
            if scheme.lower() != 'bearer':
                raise credentials_exception
            if not payload.get('sub'):
                raise credentials_exception

            user = await user_service.get_user(User.username == payload.get('sub'))
            if not user:
                raise credentials_exception
            request.scope['user'] = user
            return user
        except jwt.exceptions.PyJWTError as e:
            raise credentials_exception


security_auth = JwtAuthentication(scheme="Bearer", description="Bearer token", scheme_name='Authorization')
