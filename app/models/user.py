from datetime import datetime, date
from typing import Optional

from sqlalchemy import String, Integer, DateTime, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .mixins import BaseMixin, IdMixin, IsActiveMixin
from .base import Base


class User(Base, BaseMixin):
    __tablename__ = 'user'
    username: Mapped[str] = mapped_column(String(length=255), unique=True)
    email: Mapped[str] = mapped_column(String(length=255), unique=True)
    first_name: Mapped[str] = mapped_column(String(length=255))
    last_name: Mapped[str] = mapped_column(String(length=255))
    phone: Mapped[str] = mapped_column(String(length=15))

    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_staff: Mapped[bool] = mapped_column(default=False)
    is_verified: Mapped[bool] = mapped_column(default=True)
    hashed_password: Mapped[str] = mapped_column(String(1024), nullable=False)
