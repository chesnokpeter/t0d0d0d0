from dataclasses import dataclass, field
from ...domain.services import ProjectService
from ...domain.schemas import NewProjectSch
from ...domain import ProjectModel
from .base import BaseUseCase

from ...presentation import ServiceReturn, ServiceRetModel
from ...domain.repos import AbsUserRepo, AbsEncryptionRepo, BaseRepo, AbsProjectRepo


@dataclass(eq=False)
class BaseProjectUseCase(BaseUseCase):
    service: ProjectService

    async def execute(self): ...


@dataclass(eq=False)
class NewProjUseCase(BaseProjectUseCase):
    repo_used: list[BaseRepo] = field(default_factory=lambda: [AbsUserRepo, AbsEncryptionRepo, AbsProjectRepo], init=False)

    async def execute(self, user_id: int, data: NewProjectSch) -> ServiceRetModel[ProjectModel]:
        res = await self.call_with_service_excepts(lambda: self.service.new(user_id, data))

        return self.sret.ret('new project', 'successfully created new project', res, ['name']), res


@dataclass(eq=False)
class AllProjectsUseCase(BaseProjectUseCase):
    repo_used: list[BaseRepo] = field(default_factory=lambda: [AbsUserRepo, AbsProjectRepo], init=False)

    async def execute(self, user_id: int) -> ServiceRetModel[list[ProjectModel | None]]:
        res = await self.call_with_service_excepts(lambda: self.service.get_all(user_id))

        if not res:
            return self.sret.ret('projects not found', 'not found your projects', []), []

        return self.sret.ret('list projects', 'successfully listed projects', res, ['name']), res


@dataclass(eq=False)
class EditProjectUseCase(BaseProjectUseCase):
    repo_used: list[BaseRepo] = field(default_factory=lambda: [AbsUserRepo, AbsProjectRepo, AbsEncryptionRepo], init=False)

    async def execute(self, user_id: int, project_id: int, **data) -> ServiceRetModel[ProjectModel]:
        res = await self.call_with_service_excepts(lambda: self.service.edit(user_id, project_id, **data))

        return self.sret.ret('edit project', 'successfully edit project', res, ['name']), res



@dataclass(eq=False)
class DeleteProjectUseCase(BaseProjectUseCase):
    repo_used: list[BaseRepo] = field(default_factory=lambda: [AbsUserRepo, AbsProjectRepo], init=False)

    async def execute(self, user_id: int, project_id: int) -> ServiceReturn:
        res = await self.call_with_service_excepts(lambda: self.service.delete(user_id, project_id))

        return self.sret.ret('deleted project', 'successfully deleted project', [])
