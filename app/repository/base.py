from sqlalchemy import select, update, insert
from typing import TypeVar, Type, Sequence

from app.backend.session import async_session_maker
from app.models import Base

M = TypeVar('M', bound=Base)


class BaseRepository:
    def __init__(self, model: Type[M]):
        self.model = model
        self.scalar = True

    async def retrieve(self, *clauses, **filters):
        stmt = (
            select(self.model)
            .where(*clauses)
            .filter_by(**filters)
        )
        async with async_session_maker() as session:
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def create(self, instance=None, *args, **kwargs):
        '''create with orm session.add(instance)'''
        instance = instance or self.model(**kwargs)

        async with async_session_maker() as session:
            session.add(instance)
            await session.commit()
            # await session.refresh(instance)
            return instance

    async def list(self, *clauses, **filters) -> Sequence[M]:
        stmt = (
            select(self.model)
            .where(*clauses)
            .filter_by(**filters)
        )
        async with async_session_maker() as session:
            results = await session.execute(stmt)
            return results.scalars().all() if self.scalar else results.fetchall()

    async def insert(self, data):
        '''create with insert() stmt, returning id'''
        stmt = insert(self.model).values(data).returning(self.model.id)
        async with async_session_maker() as session:
            result = await session.execute(stmt)
            return result

    async def update(self, data: dict, *clauses, **filters):
        stmt = (update(self.model).where(*clauses)
                .filter_by(**data)
                .values(**filters)
                .returning(self.model.id))
        async with async_session_maker() as session:
            return await session.execute(stmt)

    async def exists(self, *clauses, **filters):
        query = (select(self.model)
                 .where(*clauses)
                 .filter_by(**filters)
                 .exists())
        async with async_session_maker() as session:
            return (await session.execute(select(query))).scalar_one_or_none()
