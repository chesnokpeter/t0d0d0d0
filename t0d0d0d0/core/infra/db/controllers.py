from typing import List, Type, TypeVar, Generic, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, update, insert
from t0d0d0d0.core.infra.db.tables import USER, AbsMODEL, PROJECT, TASK

from abc import ABC, abstractmethod

class AbsController(ABC):
    model: AbsMODEL
    @abstractmethod
    def __init__(self): raise NotImplementedError
    @abstractmethod
    async def get(self): raise NotImplementedError
    @abstractmethod
    async def get_one(self): raise NotImplementedError
    @abstractmethod
    async def offset(self): raise NotImplementedError
    @abstractmethod
    async def update(self): raise NotImplementedError

T = TypeVar('T')

class Controller(Generic[T]):   
    model: Type[T]
    def __init__(self, session: Session):
        self.session = session
    async def get(self, **data) -> Optional[List[T]]:
        result = await self.session.execute(select(self.model).filter_by(**data))
        return [i[0] for i in result.all()]
    async def get_one(self, **data) -> Optional[T]:
        stmt = select(self.model).filter_by(**data)
        res = await self.session.execute(stmt)
        res = res.first()
        return res[0] if res else res
    async def add(self, **data) -> T:
        stmt = insert(self.model).values(**data)
        stmt = stmt.returning(self.model)
        return await self.session.scalar(stmt)
    async def offset(self, offset: int = 0, limit: int = 10, order = None, **data) -> List[List[Optional[T]]]:
        stmt = select(self.model).offset(offset).limit(limit).order_by(order).filter_by(**data)
        res = await self.session.execute(stmt)
        res = res.all()
        return res
    async def update(self, id: int, **data) -> T:
        query = (
            update(self.model)
            .where(self.model.id == id )
            .values(**data)
            .returning(self.model)
        ) 
        return await self.session.scalar(query)


class UserController(Controller[USER]):
    model = USER

class TaskController(Controller[TASK]):
    model = TASK

class ProjectController(Controller[PROJECT]):
    model = PROJECT

