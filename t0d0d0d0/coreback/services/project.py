from typing import Annotated, TypeAlias

from t0d0d0d0.coreback.exceptions import UserException, ProjectException
from t0d0d0d0.coreback.models.project import ProjectModel
from t0d0d0d0.coreback.schemas.project import NewProjectSch
from t0d0d0d0.coreback.services.abstract import AbsService
from t0d0d0d0.coreback.uow import BaseUnitOfWork, UnitOfWork, uowaccess

UnitOfWork: TypeAlias = Annotated[BaseUnitOfWork, UnitOfWork]


class ProjectService(AbsService):
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    @uowaccess('user', 'project')
    async def new(self, user_id: int, data: NewProjectSch) -> ProjectModel:
        async with self.uow:
            u = await self.uow.user.get_one(id=user_id)
            if not u:
                raise UserException('user not found')

            p = await self.uow.project.add(**data.model_dump(), user_id=user_id)
            await self.uow.commit()
            return ProjectModel(**p.model().model_dump())

    @uowaccess('user', 'project')
    async def getAll(self, user_id: int) -> list[ProjectModel]:
        async with self.uow:
            u = await self.uow.user.get_one(id=user_id)
            if not u:
                raise UserException('user not found')
            t = await self.uow.project.get(user_id=user_id)
            return [ProjectModel(**i.model().model_dump()) for i in t]

    @uowaccess('user', 'project')
    async def edit(self, user_id: int, project_id: int, **data) -> None:
        async with self.uow:
            u = await self.uow.user.get_one(id=user_id)
            if not u:
                raise UserException('user not found')
            p = await self.uow.project.get_one(id=project_id)
            if not p:
                raise ProjectException('project not found')
            await self.uow.project.update(project_id, **data)
            await self.uow.commit()

    @uowaccess('user', 'project')
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
