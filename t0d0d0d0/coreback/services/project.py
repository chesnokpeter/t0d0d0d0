from t0d0d0d0.coreback.exceptions import UserException, ProjectException
from t0d0d0d0.coreback.models.project import ProjectModel
from t0d0d0d0.coreback.schemas.project import NewProjectSch
from t0d0d0d0.coreback.services.abstract import AbsService
from t0d0d0d0.coreback.uow import uowaccess
from t0d0d0d0.coreback.encryption import rsa_encrypt, rsa_public_deserial
from t0d0d0d0.coreback.state import Repos


class ProjectService(AbsService):
    @uowaccess(Repos.USER, Repos.PROJECT)
    async def new(self, user_id: int, data: NewProjectSch) -> ProjectModel:
        async with self.uow:
            u = await self.uow.user.get_one(id=user_id)
            if not u:
                raise UserException('user not found')

            name = rsa_encrypt(data.name, rsa_public_deserial(u.public_key))
            p = await self.uow.project.add(**data.model_dump(exclude=['name']), name=name, user_id=user_id)
            await self.uow.commit()
            return ProjectModel(**p.model().model_dump())

    @uowaccess(Repos.USER, Repos.PROJECT)
    async def getAll(self, user_id: int) -> list[ProjectModel]:
        async with self.uow:
            u = await self.uow.user.get_one(id=user_id)
            if not u:
                raise UserException('user not found')
            t = await self.uow.project.get(user_id=user_id)
            return [ProjectModel(**i.model().model_dump()) for i in t]

    @uowaccess(Repos.USER, Repos.PROJECT)
    async def edit(self, user_id: int, project_id: int, **data) -> None:
        async with self.uow:
            u = await self.uow.user.get_one(id=user_id)
            if not u:
                raise UserException('user not found')
            p = await self.uow.project.get_one(id=project_id)
            if not p:
                raise ProjectException('project not found')
            if data.get('name'):
                data['name'] = rsa_encrypt(data['name'], rsa_public_deserial(u.public_key))
            await self.uow.project.update(project_id, **data)
            await self.uow.commit()

    @uowaccess(Repos.USER, Repos.PROJECT)
    async def delete(self, user_id: int, project_id: int) -> None:
        async with self.uow:
            u = await self.uow.user.get_one(id=user_id)
            if not u:
                raise UserException('user not found')

            t = await self.uow.project.get_one(id=project_id)
            if not t:
                raise ProjectException('project not found')

            if t.user_id != user_id:
                raise UserException('user has no control of the project')

            await self.uow.project.delete(id=project_id)
            await self.uow.commit()
