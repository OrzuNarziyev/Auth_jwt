from fastapi import Request, HTTPException
from fastapi.security.utils import get_authorization_scheme_param

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import (Send, Scope, Receive, ASGIApp, Message)


class AuthenticationMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, paths: list[str]):
        super().__init__(app)
        self.paths = paths

    async def dispatch(self, request: Request, call_next):
        if not request.url.path in self.paths:
            authorization = request.cookies.get('access_token') or request.headers.get('Authorization')
            schema, credentials = get_authorization_scheme_param(authorization)
            credential_exception = HTTPException(
                status_code=401,
                detail="Invalid authentication credentials.",
            )
            if not all([authorization, schema, credentials]):
                raise credential_exception
            # TODO: add logic authentication user request.scope['user'] = user
            user = None
            request.scope['user'] = user

        return await call_next(request)
