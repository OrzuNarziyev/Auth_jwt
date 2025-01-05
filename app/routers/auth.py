from typing import Optional
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Request, Response, Depends, HTTPException, status
from datetime import datetime, timedelta, tzinfo
from app.backend.config import settings
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth import auth_service

router = APIRouter()


@router.post("/token", response_model=TokenResponse)
async def login(body: LoginRequest, response: Response):
    token = await auth_service.login(body)
    if token:
        response.set_cookie('access_token',
                            f"{token.token_type} {token.access_token}",
                            httponly=True,
                            samesite='strict',
                            max_age=settings.access_token_lifetime.seconds - 30,
                            )
    return token


@router.post("/token/refresh")
async def token_refresh(token: str, response: Response):
    token = await auth_service.refresh_token(token)
    if token:
        response.set_cookie('access_token',
                            f"{token.token_type} {token.access_token}",
                            httponly=True,
                            samesite='strict',
                            max_age=settings.access_token_lifetime.seconds - 30,
                            )
    print(token)
    return token


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"msg": "Successfully logged out"}
