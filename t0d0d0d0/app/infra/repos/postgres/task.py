from .base import PostgresDefaultRepo
from ...utils.postgres import TASK
from ....domain.repos import AbsTaskRepo
from ....domain.models import TaskModel, TaskModelWithProjName

from sqlalchemy import delete, insert, select, update

class TaskRepoPostgresql(PostgresDefaultRepo[TaskModel], AbsTaskRepo):
    table = TASK

    #! get_all_with_proj_name implement!!


    async def get_all_with_proj_name(self, **data): 
        result = await self.session.execute(
            select(self.table).order_by(self.table.id.desc()).filter_by(**data)
        )  # type: ignore
        result = result.all()
        # return [i[0].model() for i in result]
        return [TaskModelWithProjName(            
            id=i.id,
            name=i.name,
            createdate=i.createdat,
            date=i.date,
            time=i.time,
            status=i.status,
            user_id=i.user_id,
            project_id=i.project_id,
            project_name='ЙОООУ') for i in result]