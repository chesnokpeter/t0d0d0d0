from dataclasses import dataclass

from .exceptions import NotFoundError, ConflictError
from ..models import ProjectModel
from ..entities import AddProject
from ..schemas import NewProjectSch
from ..repos import AbsUserRepo, AbsEncryptionRepo, AbsProjectRepo

@dataclass(eq=False)
class ProjectService:
    user_repo: AbsUserRepo
    project_repo: AbsProjectRepo
    encryption_repo: AbsEncryptionRepo

    async def new(self, user_id: int, data: NewProjectSch) -> ProjectModel:
        u = await self.user_repo.get(user_id)
        if not u:
            raise NotFoundError('user not found')

        name = self.encryption_repo.rsa_encrypt(data.name, self.encryption_repo.rsa_public_deserial(u.public_key))
        p = AddProject(name, user_id)
        return await self.project_repo.add(p)

    async def get_all(self, user_id: int) -> list[ProjectModel] | None:
        u = await self.user_repo.get(id=user_id)
        if not u:
            raise NotFoundError('user not found')

        return await self.project_repo.get_all(user_id=user_id)
    
    async def edit(self, user_id: int, project_id: int, **data) -> ProjectModel:
        u = await self.user_repo.get(user_id)
        if not u:
            raise NotFoundError('user not found')
        p = await self.project_repo.get(id=project_id)
        if not p:
            raise NotFoundError('project not found')
        
        if data.get('name'):
            data['name'] = self.encryption_repo.rsa_encrypt(data['name'], self.encryption_repo.rsa_public_deserial(u.public_key))
        p = AddProject(**data, user_id=user_id)
        return await self.project_repo.update(project_id, p)
    
    async def delete(self, user_id: int, project_id: int) -> None:
        u = await self.user_repo.get(user_id)
        if not u:
            raise NotFoundError('user not found')
        p = await self.project_repo.get(project_id)
        if not p:
            raise NotFoundError('project not found')

        if p.user_id != user_id:
            raise ConflictError('user has not control of this project')

        await self.project_repo.delete(project_id)
