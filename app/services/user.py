from app.models import User
from app.repository.user import user_repository


class UserService:

    async def get_user(self, *args, **kwargs):
        return await user_repository.retrieve(*args, **kwargs)

    async def create_user(self, data) -> User:
        return await user_repository.create(**data)

    async def create_user_with_pin(self, pin: str) -> User:
        ...


user_service = UserService()
