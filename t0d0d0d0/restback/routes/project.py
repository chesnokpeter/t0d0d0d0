from fastapi import APIRouter, Depends, Security, Body

from t0d0d0d0.coreback.schemas.project import NewProjectSch
from t0d0d0d0.coreback.services.project import ProjectService
from t0d0d0d0.restback.answer import Answer
from t0d0d0d0.restback.depends import accessSecure, uowdep, project, user

projectRouter = APIRouter(prefix='/project', tags=['project'])


@projectRouter.post('/new')
async def new_project(
    data: NewProjectSch,
    uow = Depends(uowdep(user, project)),
    credentials = Security(accessSecure),
):
    s = await ProjectService(uow).new(user_id=int(credentials['id']), data=data)
    r = Answer.OkAnswerModel('project', 'project', data=s)
    return r.response


@projectRouter.get('/get')
async def get_user_projects(uow=Depends(uowdep(user, project)), credentials=Security(accessSecure)):
    s = await ProjectService(uow).getAll(user_id=int(credentials['id']))
    r = Answer.OkAnswerModel('project', 'project', data=s)
    return r.response


@projectRouter.patch('/edit/name')
async def edit_project(
    id: int = Body(embed=True),
    name: str = Body(embed=True),
    uow=Depends(uowdep(user, project)),
    credentials=Security(accessSecure),
):
    await ProjectService(uow).edit(user_id=int(credentials['id']), project_id=id, name=name)
    r = Answer.OkAnswer('project', 'project', data=[{}])
    return r.response


@projectRouter.delete('/delete')
async def delete_project(
    id: int = Body(embed=True),
    uow=Depends(uowdep(user, project)),
    credentials=Security(accessSecure),
):
    await ProjectService(uow).delete(user_id=int(credentials['id']), project_id=id)
    r = Answer.OkAnswer('project', 'project', data=[{}])
    return r.response
