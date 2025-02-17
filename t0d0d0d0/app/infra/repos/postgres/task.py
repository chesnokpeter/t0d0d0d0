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
            id=i[0].id,
            name=i[0].name,
            createdate=i[0].createdat,
            date=i[0].date,
            time=i[0].time,
            status=i[0].status,
            user_id=i[0].user_id,
            project_id=i[0].project_id,
            project_name='ЙОООУ') for i in result]