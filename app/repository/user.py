from sqlalchemy import select, text
from sqlalchemy.orm import selectinload, contains_eager, aliased, Load
from .base import BaseRepository
from ..backend.session import async_session_maker

from app.models.user import User


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(model=User)

    async def get_user(self, *clauses, **filters):
        async with async_session_maker() as session:
            stmt = (
                select(self.model)
                .filter(*clauses)
                .filter(*filters)
                .options(
                    Load(self.model).load_only(
                        self.model.id, self.model.first_name,
                        self.model.last_name, self.model.middle_name,
                        self.model.phone

                    )
                )
            )
            user = await session.execute(stmt)
            return user.scalar_one_or_none()

user_repository = UserRepository()
