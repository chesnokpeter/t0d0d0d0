from t0d0d0d0.coreback.services.abstract import AbsService

from t0d0d0d0.coreback.models.project import ProjectModel 
from t0d0d0d0.coreback.schemas.project import NewProjectSch
from t0d0d0d0.coreback.uow import BaseUnitOfWork
from t0d0d0d0.coreback.exceptions import AuthException, ProjectException

class ProjectService(AbsService): 
    def __init__(self, uow: BaseUnitOfWork) -> None:
        self.uow = uow

    async def new(self, user_id:int, data:NewProjectSch) -> ProjectModel:
        """required: database"""
        async with self.uow:
            u = await self.uow.user.get_one(id=user_id)
            if not u: raise AuthException('User not found')

            p = await self.uow.project.add(**data.model_dump(), user_id=user_id)
            await self.uow.commit()
            return ProjectModel(**p.model().model_dump())
        
    async def getAll(self, user_id:int) -> list[ProjectModel]:
        """required: database"""
        async with self.uow:
            u = await self.uow.user.get_one(id=user_id)
            if not u: raise AuthException('User not found')
            t = await self.uow.project.get(user_id=user_id)
            return [ProjectModel(**i.model().model_dump()) for i in t]
        