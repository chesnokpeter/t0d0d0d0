from t0d0d0d0.core.infra.db.models import CleanProjectModel, NewProjectModel, IdCleanProjectModel
from t0d0d0d0.core.schemas.project import NewProjectSch
from t0d0d0d0.core.uow import UnitOfWork
from t0d0d0d0.core.exceptions import AuthException, ProjectException

class ProjectService: 
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def newProject(self, user_id:int, data:NewProjectSch) -> CleanProjectModel:
        """required: database"""
        async with self.uow:
            u = await self.uow.user.get_one(id=user_id)
            if not u: raise AuthException('User not found')

            p = NewProjectModel(**data.model_dump(), user_id=user_id)

            p = await self.uow.project.add(**p.model_dump())
            await self.uow.commit()
            return CleanProjectModel(**p.model().model_dump())
        
    async def getProjects(self, user_id:int) -> list[IdCleanProjectModel]:
        """required: database"""
        async with self.uow:
            u = await self.uow.user.get_one(id=user_id)
            if not u: raise AuthException('User not found')
            t = await self.uow.project.get(user_id=user_id)
            return [IdCleanProjectModel(**i.model().model_dump()) for i in t]
        