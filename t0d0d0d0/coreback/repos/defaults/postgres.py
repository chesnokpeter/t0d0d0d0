from typing import List, Type, TypeVar, Generic
from sqlalchemy.orm import Session
from sqlalchemy import select, update, insert, delete

from t0d0d0d0.coreback.repos.abstract import DbAbsRepo
from t0d0d0d0.coreback.infra.abstract import DbAbsTable

T = TypeVar('T', bound=DbAbsTable)

class PostgresDefaultRepo(Generic[T], DbAbsRepo):   
    model: Type[T]
    def __init__(self, session: Session):
        self.session = session
    async def get(self, **data) -> List[T] | None:
        result = await self.session.execute(select(self.model).filter_by(**data)) # type: ignore
        return [i[0] for i in result.all()]
    async def get_one(self, **data) -> T | None:
        stmt = select(self.model).filter_by(**data)
        res = await self.session.execute(stmt) # type: ignore
        res = res.first()
        return res[0] if res else res
    async def add(self, **data) -> T:
        stmt = insert(self.model).values(**data)
        stmt = stmt.returning(self.model)
        return await self.session.scalar(stmt) # type: ignore
    async def offset(self, offset: int = 0, limit: int | None = None, order = None, **data) -> List[T] | None:
        stmt = select(self.model).offset(offset).limit(limit).order_by(order).filter_by(**data)
        res = await self.session.execute(stmt) # type: ignore
        res = res.all()
        return [i[0] for i in res]
    async def update(self, id: int, **data) -> T:
        query = (
            update(self.model)
            .where(self.model.id == id )
            .values(**data)
            .returning(self.model)
        ) 
        return await self.session.scalar(query) # type: ignore
    async def delete(self, id:int):
        stmt = (delete(self.model).where(self.model.id==id)) # type: ignore
        await self.session.execute(stmt) # type: ignore