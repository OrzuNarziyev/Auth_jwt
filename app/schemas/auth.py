from typing import Annotated

from pydantic import BaseModel, Field, AfterValidator
from typing_extensions import Optional


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = 'Bearer'


class LoginRequest(BaseModel):
    username: Optional[str] = None
    phone: Optional[str] = None
    password: str

