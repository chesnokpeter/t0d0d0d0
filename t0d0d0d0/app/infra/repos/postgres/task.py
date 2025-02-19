from .base import PostgresDefaultRepo
from ...utils.postgres import TASK
from ....domain.repos import AbsTaskRepo
from ....domain.models import TaskModel, TaskModelWithProjName

from sqlalchemy import select
from sqlalchemy.orm import selectinload

class TaskRepoPostgresql(PostgresDefaultRepo[TaskModel], AbsTaskRepo):
    table = TASK


    async def get_all_with_proj_name(self, **data): 
        result = await self.session.execute(
            select(self.table).order_by(self.table.id.desc()).filter_by(**data).options(selectinload(TASK.project))
        )  # type: ignore
        result = result.all()
        return [TaskModelWithProjName(            
            id=i[0].id,
            name=i[0].name,
            createdate=i[0].createdat,
            date=i[0].date,
            time=i[0].time,
            status=i[0].status,
            user_id=i[0].user_id,
            project_id=i[0].project_id,
            project_name=i[0].project.name if i[0].project else None) for i in result]
