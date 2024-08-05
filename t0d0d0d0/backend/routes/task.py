from fastapi import APIRouter, Security
from t0d0d0d0.core.depends import uowdep
from t0d0d0d0.core.infra.db.models import CleanTaskModel, CleanGetTasksModel
from t0d0d0d0.backend.answer import Answer, AnswerResModel
from t0d0d0d0.core.schemas.task import NewTaskSch
from t0d0d0d0.core.services.task import TaskService
from t0d0d0d0.core.depends import accessSecure, infra
import pprint
taskRouter = APIRouter(prefix='/task', tags=['task'])

@taskRouter.post('/newTask', response_model=AnswerResModel[CleanTaskModel]) 
async def new_task(data:NewTaskSch, uow=uowdep(infra()), credentials = Security(accessSecure)):
    s = await TaskService(uow).newTask(user_id=int(credentials["id"]), data=data)
    r = Answer.OkAnswerModel('task', 'task', data=s)
    return r.response


@taskRouter.get('/getInbox', response_model=AnswerResModel[CleanTaskModel]) 
async def get_inbox(uow=uowdep(infra()), credentials = Security(accessSecure)):
    s = await TaskService(uow).getInbox(user_id=int(credentials["id"]))
    r = Answer.OkAnswerModel('task', 'task', data=s)
    return r.response



@taskRouter.get('/getTasks') 
async def get_inbox(uow=uowdep(infra()), credentials = Security(accessSecure)):
    s = await TaskService(uow).getTasks(user_id=int(credentials["id"]))
    r = Answer.OkAnswerModel('task', 'task', data=s)
    for i in r.data:
        r.data[-1][i['date']] = [i] if not r.data[-1].get(i['date']) else r.data[-1][i['date']].append(i)
    pprint.pprint(r.data)
    return r.response


