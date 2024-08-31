from typing import List, Type, TypeVar, Generic, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, update, insert, delete
from t0d0d0d0.coreback.infra.db.models import USER, AbsModel, PROJECT, TASK

class AbsRepository:
    model: AbsModel
    def __init__(self): ...
    async def get(self): raise NotImplementedError
    async def get_one(self): raise NotImplementedError
    async def add(self): raise NotImplementedError
    async def offset(self): raise NotImplementedError
    async def update(self): raise NotImplementedError
    async def delete(self): raise NotImplementedError

T = TypeVar('T', bound=AbsModel)

class Repository(Generic[T], AbsRepository):   
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



class UserRepository(Repository[USER]):
    model = USER

class TaskRepository(Repository[TASK]):
    model = TASK
    async def get_by_date(self, offset: int = 0, limit: int | None = None, order = None, **data) -> Optional[List[TASK]]:
        stmt = select(self.model).offset(offset).limit(limit).order_by(self.model.date.desc()).filter_by(**data).filter(self.model.date.isnot(None))
        res = await self.session.execute(stmt) # type: ignore
        res = res.all()
        return [i[0] for i in res]


class ProjectRepository(Repository[PROJECT]):
    model = PROJECT

