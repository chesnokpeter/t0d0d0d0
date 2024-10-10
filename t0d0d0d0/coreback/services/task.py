import datetime
from datetime import date as datetype
from typing import Annotated, TypeAlias

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
from t0d0d0d0.coreback.uow import BaseUnitOfWork, UnitOfWork, uowaccess

UnitOfWork: TypeAlias = Annotated[BaseUnitOfWork, UnitOfWork]


class TaskService(AbsService):
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    @uowaccess('user', 'task', 'project')
    async def new(self, user_id: int, data: NewTaskSch) -> TaskModel:
        async with self.uow:
            u = await self.uow.user.get_one(id=user_id)
            if not u:
                raise UserException('user not found')

            if data.project_id:
                p = await self.uow.project.get_one(id=data.project_id)
                if not p:
                    raise ProjectException('project not found')

            t = await self.uow.task.add(**data.model_dump(), user_id=user_id)
            await self.uow.commit()
            return t.model()

    @uowaccess('user', 'task')
    async def getInbox(self, user_id: int) -> list[TaskModel]:
        async with self.uow:
            u = await self.uow.user.get_one(id=user_id)
            if not u:
                raise UserException('user not found')

            t = await self.uow.task.get(user_id=user_id, project_id=None, date=None, time=None)
            return [TaskModel(**i.model().model_dump()) for i in t]

    @uowaccess('user', 'task')
    async def getAll(self, user_id: int) -> list[TaskModel]:
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

    @uowaccess('user', 'task')
    async def getByDate(self, user_id: int, date: datetype) -> list[TaskModel]:
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

    @uowaccess('user', 'task')
    async def getById(self, user_id: int, id: str) -> TaskModel | None:
        async with self.uow:
            u = await self.uow.user.get_one(id=user_id)
            if not u:
                raise UserException('user not found')

            t = await self.uow.task.get_one(user_id=user_id, id=id)
            if t:
                return t.model()
            return None

    @uowaccess('user', 'task', 'shedulernotify')
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

    @uowaccess('user', 'task')
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
