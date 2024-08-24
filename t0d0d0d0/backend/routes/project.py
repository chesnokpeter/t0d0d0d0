from fastapi import APIRouter, Security
from t0d0d0d0.core.depends import uowdep
from t0d0d0d0.backend.answer import Answer
from t0d0d0d0.core.schemas.project import NewProjectSch
from t0d0d0d0.core.services.project import ProjectService
from t0d0d0d0.core.depends import accessSecure, infra

projectRouter = APIRouter(prefix='/project', tags=['project'])

@projectRouter.post('/new/project') 
async def new_project(data:NewProjectSch, uow=uowdep(infra()), credentials = Security(accessSecure)):
    s = await ProjectService(uow).newProject(user_id=int(credentials["id"]), data=data)
    r = Answer.OkAnswerModel('project', 'project', data=s)
    return r.response


@projectRouter.get('/get/projects') 
async def new_project( uow=uowdep(infra()), credentials = Security(accessSecure)):
    s = await ProjectService(uow).getProjects(user_id=int(credentials["id"]))
    r = Answer.OkAnswerModel('project', 'project', data=s)
    return r.response


