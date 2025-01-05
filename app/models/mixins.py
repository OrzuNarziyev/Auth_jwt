import locale
from gettext import gettext
from typing import Annotated
from datetime import datetime
from sqlalchemy import text, Boolean
from sqlalchemy.orm import mapped_column, Mapped

intpk = Annotated[int, mapped_column(primary_key=True, sort_order=-1, autoincrement=True)]
created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"),
    onupdate=datetime.utcnow,
)]
is_active = Annotated[bool, mapped_column(Boolean, default=True)]


def get_locale() -> str:
    return 'uz'


class IdMixin(object):
    id: Mapped[intpk]


class IsActiveMixin(object):
    is_active: Mapped[is_active]


class IDIsActiveMixin:
    id: Mapped[intpk]
    is_active: Mapped[is_active]


class BaseMixin(object):
    id: Mapped[intpk]

    is_active: Mapped[is_active]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
