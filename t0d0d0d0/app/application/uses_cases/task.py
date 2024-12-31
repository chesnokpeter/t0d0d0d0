from dataclasses import dataclass
from ...domain.services import TaskService
from ...domain.schemas import NewTaskSch
from .base import BaseUseCase

from ...presentation import ServiceReturn

@dataclass(eq=False, slots=True)
class BaseTaskUseCase(BaseUseCase):
    service: TaskService


@dataclass(eq=False, slots=True)
class NewTaskUseCase(BaseTaskUseCase):
    async def execute(self, user_id: int, data: NewTaskSch) -> ServiceReturn:
        res = await self.call_with_service_excepts(lambda: self.service.new(user_id, data))

        return ServiceReturn.OkAnswerModel('new task', 'successfully created new task', res, ['name'])


@dataclass(eq=False, slots=True)
class EditTaskUseCase(BaseTaskUseCase):
    async def execute(self, user_id: int, task_id: int, **data) -> ServiceReturn:
        res = await self.call_with_service_excepts(lambda: self.service.edit(user_id, task_id, **data))

        return ServiceReturn.OkAnswerModel('edit task', 'successfully edit task', res, ['name'])



@dataclass(eq=False, slots=True)
class DeleteTaskUseCase(BaseTaskUseCase):
    async def execute(self, user_id: int, task_id: int) -> ServiceReturn:
        res = await self.call_with_service_excepts(lambda: self.service.delete(user_id, task_id))

        return ServiceReturn.OkAnswer('deleted project', 'successfully deleted project', [])


@dataclass(eq=False, slots=True)
class AllTaskUseCase(BaseTaskUseCase):
    async def execute(self, user_id: int) -> ServiceReturn:
        res = await self.call_with_service_excepts(lambda: self.service.get_all(user_id))
        if not res:
            return ServiceReturn.OkAnswer('tasks not found', 'not found your tasks', [])

        return ServiceReturn.OkAnswerModel('list tasks', 'successfully listed tasks', res, ['name', 'project_name'])

@dataclass(eq=False, slots=True)
class AllInboxUseCase(BaseTaskUseCase):
    async def execute(self, user_id: int) -> ServiceReturn:
        res = await self.call_with_service_excepts(lambda: self.service.get_inbox(user_id))
        if not res:
            return ServiceReturn.OkAnswer('inbox not found', 'not found your inbox', [])

        return ServiceReturn.OkAnswerModel('list inbox', 'successfully listed inbox', res, ['name'])


@dataclass(eq=False, slots=True)
class TaskByIdUseCase(BaseTaskUseCase):
    async def execute(self, user_id: int, task_id: int) -> ServiceReturn:
        res = await self.call_with_service_excepts(lambda: self.service.get_by_id(user_id, task_id))
        return ServiceReturn.OkAnswerModel('task', 'successfully received task', res, ['name'])

