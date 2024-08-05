from t0d0d0d0.core.infra.db.models import TaskModel, NewTaskModel, CleanTaskModel, CleanGetTasksModel
from t0d0d0d0.core.schemas.task import NewTaskSch
from t0d0d0d0.core.uow import UnitOfWork
from t0d0d0d0.core.exceptions import AuthException, ProjectException

class TaskService: 
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def newTask(self, user_id:int, data:NewTaskSch) -> CleanTaskModel:
        """required: database"""
        async with self.uow:
            u = await self.uow.user.get_one(id=user_id)
            if not u: raise AuthException('User not found')

            if data.project_id:
                p = await self.uow.project.get_one(id=data.project_id)
                if not p: raise ProjectException('Project not found')

            t = NewTaskModel(**data.model_dump(), user_id=user_id)

            t = await self.uow.task.add(**t.model_dump())
            await self.uow.commit()
            return CleanTaskModel(**t.model().model_dump())

    async def getInbox(self, user_id:int) -> list[CleanTaskModel]:
        """required: database"""
        async with self.uow:
            u = await self.uow.user.get_one(id=user_id)
            if not u: raise AuthException('User not found')
            t = await self.uow.task.get(user_id=user_id, project_id=None, date=None, time=None)
            return [CleanTaskModel(**i.model().model_dump()) for i in t]
        
    async def getTasks(self, user_id:int) -> list[CleanGetTasksModel]:
        """required: database"""
        async with self.uow:
            u = await self.uow.user.get_one(id=user_id)
            if not u: raise AuthException('User not found')
            t = await self.uow.task.get_by_date(user_id=user_id)
            r = [CleanGetTasksModel(**i.model().model_dump(), project_name=i.project.name) if i.project else CleanGetTasksModel(**i.model().model_dump(), project_name=None) for i in t]
            return r