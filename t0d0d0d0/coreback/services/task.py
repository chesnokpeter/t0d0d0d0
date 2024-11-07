import datetime
from datetime import date as datetype
from t0d0d0d0.coreback.exceptions import (
    UserException,
    ProjectException,
    TaskException,
)
from t0d0d0d0.coreback.models.shedulernotify import ShedulernotifyModel
from t0d0d0d0.coreback.models.task import TaskModel
from t0d0d0d0.coreback.models.tasknotify import TasknotifyModel
from t0d0d0d0.coreback.schemas.task import NameTaskSch, NewTaskSch
from t0d0d0d0.coreback.services.abstract import AbsService
from t0d0d0d0.coreback.uow import uowaccess
from t0d0d0d0.coreback.encryption import rsa_encrypt, rsa_public_deserial

from t0d0d0d0.coreback.state import Repos


class TaskService(AbsService):
    @uowaccess(Repos.USER, Repos.TASK, Repos.PROJECT)
    async def new(self, user_id: int, data: NewTaskSch) -> TaskModel:
        async with self.uow:
            u = await self.uow.user.get_one(id=user_id)
            if not u:
                raise UserException('user not found')

            if data.project_id:
                p = await self.uow.project.get_one(id=data.project_id)
                if not p:
                    raise ProjectException('project not found')
            name = rsa_encrypt(data.name, rsa_public_deserial(u.public_key))
            t = await self.uow.task.add(**data.model_dump(exclude=['name']), name=name, user_id=user_id)
            await self.uow.commit()
        return t.model()

    @uowaccess(Repos.USER, Repos.TASK)
    async def getInbox(self, user_id: int) -> list[TaskModel]:
        async with self.uow:
            u = await self.uow.user.get_one(id=user_id)
            if not u:
                raise UserException('user not found')

            t = await self.uow.task.get(user_id=user_id, project_id=None, date=None, time=None)
        return [TaskModel(**i.model().model_dump()) for i in t]

    @uowaccess(Repos.USER, Repos.TASK)
    async def getAll(self, user_id: int) -> list[NameTaskSch]:
        async with self.uow:
            u = await self.uow.user.get_one(id=user_id)
            if not u:
                raise UserException('user not found')

            t = await self.uow.task.get_by_date(user_id=user_id)
            r = [
                NameTaskSch(**i.model().model_dump(), project_name=i.project.name)
                if i.project
                else NameTaskSch(**i.model().model_dump(), project_name=None)
                for i in t
            ]
            return r

    @uowaccess(Repos.USER, Repos.TASK)
    async def getByDate(self, user_id: int, date: datetype) -> list[NameTaskSch]:
        async with self.uow:
            u = await self.uow.user.get_one(id=user_id)
            if not u:
                raise UserException('user not found')

            t = await self.uow.task.get(user_id=user_id, date=date)
            r = [
                NameTaskSch(**i.model().model_dump(), project_name=i.project.name)
                if i.project
                else NameTaskSch(**i.model().model_dump(), project_name=None)
                for i in t
            ]
        return r

    @uowaccess(Repos.USER, Repos.TASK)
    async def getById(self, user_id: int, id: str) -> TaskModel | None:
        async with self.uow:
            u = await self.uow.user.get_one(id=user_id)
            if not u:
                raise UserException('user not found')

            t = await self.uow.task.get_one(user_id=user_id, id=id)
            if t:
                return t.model()
        return None

    @uowaccess(Repos.USER, Repos.TASK, Repos.SHEDULERNOTIFY)
    async def edit(self, user_id: int, id: str, **data) -> None:
        async with self.uow:
            u = await self.uow.user.get_one(id=user_id)
            if not u:
                raise UserException('user not found')

            t = await self.uow.task.get_one(id=id)
            if not t:
                raise TaskException('task not found')

            if t.user_id != user_id:
                raise UserException('user has no control of the task')

            if data.get('name'):
                if data['name'] == '':
                    data['name'] = ' '
                data['name'] = rsa_encrypt(data['name'], rsa_public_deserial(u.public_key))
                    
            rawt = await self.uow.task.update(id, **data)
            t = rawt.model()
            await self.uow.commit()

            if data.get('time', None):
                combined_datetime = datetime.datetime.combine(t.date, t.time)
                now = datetime.datetime.now()
                delaydelta = combined_datetime - now
                delay = delaydelta.total_seconds()
                if delay > 0:
                    tasknotify = TasknotifyModel(tgid=u.tgid, taskname=t.name, projname=rawt.project.name)
                    sheduler = ShedulernotifyModel(
                        queue_after_delay=tasknotify.queue_name,
                        delay=round(delay),
                        message=tasknotify.model_dump_json(),
                    )
                    await self.uow.shedulernotify.send(sheduler)

    @uowaccess(Repos.USER, Repos.TASK)
    async def delete(self, user_id: int, id: str) -> None:
        async with self.uow:
            u = await self.uow.user.get_one(id=user_id)
            if not u:
                raise UserException('user not found')

            t = await self.uow.task.get_one(id=id)
            if not t:
                raise TaskException('task not found')

            if t.user_id != user_id:
                raise UserException('user has no control of the task')

            await self.uow.task.delete(id=id)
            await self.uow.commit()
