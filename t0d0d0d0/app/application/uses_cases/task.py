from dataclasses import dataclass, field
from datetime import datetime
from ...domain.services import TaskService
from ...domain.schemas import NewTaskSch
from ...domain import TaskModel, TaskModelWithProjName
from .base import BaseUseCase

from ...presentation import ServiceReturn, ServiceRetModel

from ...domain.repos import AbsUserRepo, AbsEncryptionRepo, BaseRepo, AbsProjectRepo, AbsTaskRepo

@dataclass(eq=False)
class BaseTaskUseCase(BaseUseCase):
    service: TaskService


@dataclass(eq=False)
class NewTaskUseCase(BaseTaskUseCase):
    repo_used: list[BaseRepo] = field(default_factory=lambda: [AbsUserRepo, AbsTaskRepo, AbsProjectRepo, AbsEncryptionRepo], init=False)

    async def execute(self, user_id: int, data: NewTaskSch) -> ServiceRetModel[TaskModel]:
        res = await self.call_with_service_excepts(lambda: self.service.new(user_id, data))

        return self.sret.ret('new task', 'successfully created new task', res, ['name']), res


@dataclass(eq=False)
class EditTaskUseCase(BaseTaskUseCase):
    repo_used: list[BaseRepo] = field(default_factory=lambda: [AbsUserRepo, AbsTaskRepo, AbsEncryptionRepo], init=False)

    async def execute(self, user_id: int, task_id: int, **data) -> ServiceRetModel[TaskModel]:
        res = await self.call_with_service_excepts(lambda: self.service.edit(user_id, task_id, **data))

        return self.sret.ret('edit task', 'successfully edit task', res, ['name']), res



@dataclass(eq=False)
class DeleteTaskUseCase(BaseTaskUseCase):
    repo_used: list[BaseRepo] = field(default_factory=lambda: [AbsUserRepo, AbsTaskRepo], init=False)

    async def execute(self, user_id: int, task_id: int) -> ServiceReturn:
        res = await self.call_with_service_excepts(lambda: self.service.delete(user_id, task_id))

        return self.sret.ret('deleted project', 'successfully deleted project', [])


@dataclass(eq=False)
class AllTaskUseCase(BaseTaskUseCase):
    repo_used: list[BaseRepo] = field(default_factory=lambda: [AbsUserRepo, AbsTaskRepo], init=False)

    async def execute(self, user_id: int) -> ServiceRetModel[list[TaskModelWithProjName | None]]:
        res = await self.call_with_service_excepts(lambda: self.service.get_all(user_id))
        if not res:
            return self.sret.ret('tasks not found', 'not found your tasks', []), []

        return self.sret.ret('list tasks', 'successfully listed tasks', res, ['name', 'project_name']), res

@dataclass(eq=False)
class AllInboxUseCase(BaseTaskUseCase):
    repo_used: list[BaseRepo] = field(default_factory=lambda: [AbsUserRepo, AbsTaskRepo], init=False)

    async def execute(self, user_id: int) -> ServiceRetModel[list[TaskModel | None]]:
        res = await self.call_with_service_excepts(lambda: self.service.get_inbox(user_id))
        if not res:
            return self.sret.ret('inbox not found', 'not found your inbox', []), []

        return self.sret.ret('list inbox', 'successfully listed inbox', res, ['name']), res


@dataclass(eq=False)
class TaskByIdUseCase(BaseTaskUseCase):
    repo_used: list[BaseRepo] = field(default_factory=lambda: [AbsUserRepo, AbsTaskRepo], init=False)

    async def execute(self, user_id: int, task_id: int) -> ServiceRetModel[TaskModel]:
        res = await self.call_with_service_excepts(lambda: self.service.get_by_id(user_id, task_id))
        return self.sret.ret('task', 'successfully received task', res, ['name']), res

@dataclass(eq=False)
class TaskByDateUseCase(BaseTaskUseCase):
    repo_used: list[BaseRepo] = field(default_factory=lambda: [AbsUserRepo, AbsTaskRepo], init=False)

    async def execute(self, user_id: int, date: datetime) -> ServiceRetModel[list[TaskModelWithProjName | None]]:
        res = await self.call_with_service_excepts(lambda: self.service.get_by_date(user_id, date))
        return self.sret.ret('tasks', 'successfully received tasks by date', res, ['name', 'project_name']), res

