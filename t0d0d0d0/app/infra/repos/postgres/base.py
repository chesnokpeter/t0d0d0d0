from typing import Generic, Type, TypeVar, Any
from abc import ABC, abstractmethod
from dataclasses import dataclass
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session, Mapped

from ....domain.repos import BaseRepo
from ....domain.models import BaseModel
from ....shared import dtcls_slots2dict

class AbsPostgresTable(ABC):
    id: Mapped[int]
    @abstractmethod
    def model(self):
        raise NotImplementedError


@dataclass(eq=False, slots=True)
class AbsAddEntity(ABC):...

T = TypeVar('T', bound=BaseModel)


class PostgresDefaultRepo(BaseRepo[Session], Generic[T]):
    depends_on = 'PostgresConnector'
    table: Type[AbsPostgresTable]

    async def add(self, data: AbsAddEntity) -> T:
        data = dtcls_slots2dict(data)
        stmt = insert(self.table).values(**data)
        stmt = stmt.returning(self.table)
        scalar: AbsPostgresTable = await self.session.scalar(stmt)  # type: ignore
        return scalar.model()

    async def get(self, key: int) -> T | None:
        stmt = select(self.table).filter_by(id=key)
        res = await self.session.execute(stmt)  # type: ignore
        res: list[AbsPostgresTable] | None = res.first()
        return res[0].model() if res else None

    async def get_all(self, **data) -> list[T] | None:
        result = await self.session.execute(
            select(self.table).order_by(self.table.id.desc()).filter_by(**data)
        )  # type: ignore
        result: list[list[AbsPostgresTable] | None] = result.all()
        return [i[0].model() for i in result]

    async def update(self, key: int, data: AbsAddEntity) -> T:
        data = dtcls_slots2dict(data)
        query = update(self.table).where(self.table.id == key).values(**data).returning(self.table)
        scalar: AbsPostgresTable = await self.session.scalar(query)  # type: ignore
        return scalar.model()

    async def delete(self, key: int) -> None:
        stmt = delete(self.table).where(self.table.id == key)  # type: ignore
        await self.session.execute(stmt)  # type: ignore







