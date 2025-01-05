from http import HTTPStatus
from typing import Union, Optional
from fastapi.exceptions import HTTPException


class UnauthorizedException(HTTPException):

    def __init__(self, detail: str):
        super().__init__(status_code=HTTPStatus.UNAUTHORIZED, detail=detail)


class BadRequestException(HTTPException):
    default_detail = "Invalid request"

    def __init__(self, detail: Optional[str] = default_detail):
        super().__init__(status_code=HTTPStatus.BAD_REQUEST, detail=detail)


class BadRequestExceptionErrors(HTTPException):

    def __init__(self, errors: list = None, message: str = None):
        detail = {
            'message': message or 'Invalid request',
            'errors': errors,
        }
        super().__init__(status_code=HTTPStatus.BAD_REQUEST, detail=detail)


class NotFoundException(HTTPException):
    default_msg = 'Not found'

    def __init__(self, detail: Optional[str] = default_msg):
        super().__init__(status_code=HTTPStatus.NOT_FOUND, detail=detail)


class ConflictException(HTTPException):
    default_msg = 'conflict'

    def __init__(self, detail: Optional[str] = default_msg):
        super().__init__(status_code=HTTPStatus.CONFLICT, detail=detail)


class ForbiddenException(HTTPException):
    default_msg = "Permission denied"

    def __init__(self, detail: Optional[str] = default_msg):
        super().__init__(status_code=HTTPStatus.FORBIDDEN, detail=detail)


class BaseError(Exception):
    pass


class ValidationError(BaseError):

    def __init__(self, detail: str):
        super().__init__(detail)
        self.detail = detail


class NoInstanceError(BaseError):
    def __init__(self, detail: str = None, model=None):
        detail = detail or f"{model.__name__} not found"
        super().__init__(detail)
        self.detail = detail


class RequestLimitError(BaseError):
    def __init__(self, detail: str):
        super().__init__(detail)
        self.detail = detail


class PermissionError(BaseError):
    def __init__(self, detail: str = "Permission denied"):
        super().__init__(detail)
        self.detail = detail


class ImproperlyConfigured(Exception):  ...
