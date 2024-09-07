from fastapi import APIRouter, Depends, Security

from t0d0d0d0.coreback.schemas.project import NewProjectSch
from t0d0d0d0.coreback.services.project import ProjectService
from t0d0d0d0.restback.answer import Answer
from t0d0d0d0.restback.depends import accessSecure, project, uowdep, user

projectRouter = APIRouter(prefix='/project', tags=['project'])


@projectRouter.post('/new')
async def new_project(
    data: NewProjectSch,
    uow=Depends(uowdep(user, project)),
    credentials=Security(accessSecure),
):
    s = await ProjectService(uow).new(user_id=int(credentials['id']), data=data)
    r = Answer.OkAnswerModel('project', 'project', data=s)
    return r.response


@projectRouter.get('/get/all')
async def new_project(uow=Depends(uowdep(user, project)), credentials=Security(accessSecure)):
    s = await ProjectService(uow).getAll(user_id=int(credentials['id']))
    r = Answer.OkAnswerModel('project', 'project', data=s)
    return r.response
