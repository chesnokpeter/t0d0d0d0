from dataclasses import dataclass
from ...domain.services import ProjectService
from ...domain.schemas import NewProjectSch
from .base import BaseUseCase

from ...presentation import ServiceReturn


@dataclass(eq=False)
class BaseProjectUseCase(BaseUseCase):
    service: ProjectService


@dataclass(eq=False)
class NewProjUseCase(BaseProjectUseCase):
    async def execute(self, user_id: int, data: NewProjectSch) -> ServiceReturn:
        res = await self.call_with_service_excepts(lambda: self.service.new(user_id, data))

        return ServiceReturn.OkAnswerModel('new project', 'successfully created new project', res, ['name'])


@dataclass(eq=False)
class AllProjectsUseCase(BaseProjectUseCase):
    async def execute(self, user_id: int) -> ServiceReturn:
        res = await self.call_with_service_excepts(lambda: self.service.get_all(user_id))

        if not res:
            return ServiceReturn.OkAnswer('projects not found', 'not found your projects', [])

        return ServiceReturn.OkAnswerModel('list projects', 'successfully listed projects', res, ['name'])


@dataclass(eq=False)
class EditProjectUseCase(BaseProjectUseCase):
    async def execute(self, user_id: int, project_id: int, **data) -> ServiceReturn:
        res = await self.call_with_service_excepts(lambda: self.service.edit(user_id, project_id, **data))

        return ServiceReturn.OkAnswerModel('edit project', 'successfully edit project', res, ['name'])



@dataclass(eq=False)
class DeleteProjectUseCase(BaseProjectUseCase):
    async def execute(self, user_id: int, project_id: int) -> ServiceReturn:
        res = await self.call_with_service_excepts(lambda: self.service.delete(user_id, project_id))

        return ServiceReturn.OkAnswer('deleted project', 'successfully deleted project', [])
