from typing import Union

from fastapi import APIRouter, Request, Depends, Response, status, Body, Form
from pydantic import BaseModel
from sqlalchemy.sql.annotation import Annotated

from app.ext import ForbiddenException
from app.models import User
from app.services.auth import security_auth
from app.services.user import user_service

router = APIRouter(
    dependencies=[Depends(security_auth)]
)


class Pin(BaseModel):
    pin: str


@router.post("/register")
async def register(request: Request,
                   body: Pin):
    if request.user.is_superuser:
        user = await user_service.create_user_with_pin(pin=body.pin)
        return {
            'user_id': user,
        }
    else:
        raise ForbiddenException()


@router.get("/me")
async def get_user(request: Request):
    try:
        return request.user
        # return {"username": request.user.username, "email": request.user.email}
    except Exception as e:
        return request.url.path
