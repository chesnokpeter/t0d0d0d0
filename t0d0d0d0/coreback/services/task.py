from t0d0d0d0.coreback.services.abs_service import AbsService
from datetime import date as datetype
import datetime

from t0d0d0d0.coreback.infra.db.models import TaskModel
from t0d0d0d0.coreback.schemas.task import NewTaskSch, NameTaskSch
from t0d0d0d0.coreback.schemas.task import NewTaskSch
from t0d0d0d0.coreback.uow import UnitOfWork
from t0d0d0d0.coreback.exceptions import AuthException, ProjectException, TaskException

from t0d0d0d0.coreback.infra.broker.models import TasknotifyModel, ShedulernotifyModel

class TaskService(AbsService): 
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def new(self, user_id:int, data:NewTaskSch) -> TaskModel:
        """required: database"""
        async with self.uow:
            u = await self.uow.user.get_one(id=user_id)
            if not u: raise AuthException('User not found')
            if data.project_id:
                p = await self.uow.project.get_one(id=data.project_id)
                if not p: raise ProjectException('Project not found')
            t = await self.uow.task.add(**data.model_dump(), user_id=user_id)
            await self.uow.commit()
            return t.model()

    async def getInbox(self, user_id:int) -> list[TaskModel]:
        """required: database"""
        async with self.uow:
            u = await self.uow.user.get_one(id=user_id)
            if not u: raise AuthException('User not found')
            t = await self.uow.task.get(user_id=user_id, project_id=None, date=None, time=None)
            return [TaskModel(**i.model().model_dump()) for i in t]
        
    async def getAll(self, user_id:int) -> list[TaskModel]:
        """required: database"""
        async with self.uow:
            u = await self.uow.user.get_one(id=user_id)
            if not u: raise AuthException('User not found')
            t = await self.uow.task.get_by_date(user_id=user_id)
            r = [NameTaskSch(**i.model().model_dump(), project_name=i.project.name) if i.project else NameTaskSch(**i.model().model_dump(), project_name=None) for i in t]
            return r
        
    async def getByDate(self, user_id:int, date:datetype) -> list[TaskModel]:
        """required: database"""
        async with self.uow:
            u = await self.uow.user.get_one(id=user_id)
            if not u: raise AuthException('User not found')
            t = await self.uow.task.get(user_id=user_id, date=date)
            r = [NameTaskSch(**i.model().model_dump(), project_name=i.project.name) if i.project else NameTaskSch(**i.model().model_dump(), project_name=None) for i in t]
            return r
        
    async def getById(self, user_id:int, id:str) -> TaskModel | None:
        """required: database"""
        async with self.uow:
            u = await self.uow.user.get_one(id=user_id)
            if not u: raise AuthException('User not found')
            t = await self.uow.task.get_one(user_id=user_id, id=id)
            if t:return t.model()
            return None

    async def edit(self, user_id:int, id:str, **data) -> None:
        """required: database"""
        async with self.uow:
            u = await self.uow.user.get_one(id=user_id)
            if not u: raise AuthException('User not found')
            t = await self.uow.task.get_one(id=id)
            if not t: raise TaskException('task not found')
            if t.user_id != user_id: raise AuthException
            t = await self.uow.task.update(id, **data)
            t = t.model()
            await self.uow.commit()

            if data.get('time', None) or data.get('date', None):
                combined_datetime = datetime.datetime.combine(t.date, t.time)
                now = datetime.datetime.now()
                current_time = datetime.datetime.combine(now.date(), datetime.time(now.hour, now.minute))
                delaydelta = combined_datetime - current_time
                delay = delaydelta.total_seconds()
                if delay > 0:
                    tgid = await self.uow.user.get_one(id=t.user_id)
                    if tgid:
                        tgid = tgid.model().tgid
                        tasknotify = TasknotifyModel(tgid=tgid, taskname=t.name)
                        sheduler = ShedulernotifyModel(queue_after_delay=tasknotify.queue_name, delay=round(delay), message=tasknotify.model_dump_json())
                        await self.uow.sheduler.send(sheduler)
                        print('ОТПРАВЛЕНО')


    async def delete(self, user_id:int, id:str) -> None:
        """required: database"""
        async with self.uow:
            u = await self.uow.user.get_one(id=user_id)
            if not u: raise AuthException('User not found')
            t = await self.uow.task.get_one(id=id)
            if not t: raise TaskException('task not found')
            if t.user_id != user_id: raise AuthException
            await self.uow.task.delete(id=id)
            await self.uow.commit()
            