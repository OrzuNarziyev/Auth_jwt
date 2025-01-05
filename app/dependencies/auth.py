from typing import Optional
from fastapi import Request, Response, HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordBearer
from fastapi.security.base import SecurityBase
from fastapi.security.utils import get_authorization_scheme_param

from fastapi.openapi.models import HTTPBase as HTTPBaseModel

class CustomAuth(SecurityBase):
    def __init__(
            self,
            *,
            scheme: str,
            scheme_name: Optional[str] = None,
            description: Optional[str] = None,
            auto_error: bool = True,
    ):
        self.model = HTTPBaseModel(scheme=scheme, description=description)
        self.scheme_name = scheme_name or self.__class__.__name__
        self.auto_error = auto_error

    async def __call__(
            self, request: Request, responce: Response
    ) -> Optional[HTTPAuthorizationCredentials]:
        # authorization_1 = request.headers.get("Authorization")
        authorization = request.cookies.get("access_token")
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and credentials):
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            else:
                return None
        responce.delete_cookie("access_token")
        return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)


oauth2_scheme = CustomAuth(scheme="basic", scheme_name="JWTAuthentication")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    return token
