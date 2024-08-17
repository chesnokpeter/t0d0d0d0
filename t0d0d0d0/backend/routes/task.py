from fastapi import APIRouter, Security, Body
from datetime import date as datetype
from t0d0d0d0.core.depends import uowdep
from t0d0d0d0.core.infra.db.models import CleanTaskModel, IdCleanTaskModel
from t0d0d0d0.backend.answer import Answer, AnswerResModel
from t0d0d0d0.core.schemas.task import NewTaskSch
from t0d0d0d0.core.services.task import TaskService
from t0d0d0d0.core.depends import accessSecure, infra

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

@taskRouter.delete('/delTask', response_model=AnswerResModel[None]) 
async def del_task(id:int = Body(embed=True), uow=uowdep(infra()), credentials = Security(accessSecure)):
    await TaskService(uow).delTask(user_id=int(credentials["id"]), id=id)
    r = Answer.OkAnswer('task', 'task', data=[{}])
    return r.response

@taskRouter.post('/getTaskByDate', response_model=AnswerResModel[IdCleanTaskModel]) 
async def get_task_by_date(date:datetype = Body(embed=True), uow=uowdep(infra()), credentials = Security(accessSecure)):
    s = await TaskService(uow).getTaskByDate(user_id=int(credentials["id"]), date=date)
    r = Answer.OkAnswerModel('task', 'task', data=s)
    return r.response




@taskRouter.get('/getTasks', response_model=AnswerResModel[list[IdCleanTaskModel]]) 
async def get_tasks(uow=uowdep(infra()), credentials = Security(accessSecure)):
    s = await TaskService(uow).getTasks(user_id=int(credentials["id"]))
    r = Answer.OkAnswerModel('task', 'task', data=s)
    tasks = {}
    for i in r.data:
        if tasks.get(i['date']):
            tasks[i['date']].append(i)
        else:
            tasks[i['date']] = [i]
    r = Answer.OkAnswer('task', 'task', data=tasks)
    return r.response


