from t0d0d0d0.coreback.repos.defaults.postgres import PostgresDefaultRepo
from t0d0d0d0.coreback.infra.postgresql.tables import TASK

from sqlalchemy import select, update, insert, delete

class TaskRepo(PostgresDefaultRepo[TASK]):
    model = TASK
    reponame = 'task'
    async def get_by_date(self, offset: int = 0, limit: int | None = None, order = None, **data) -> list[TASK] | None:
        stmt = select(self.model).offset(offset).limit(limit).order_by(self.model.date.desc()).filter_by(**data).filter(self.model.date.isnot(None))
        res = await self.session.execute(stmt) # type: ignore
        res = res.all()
        return [i[0] for i in res]