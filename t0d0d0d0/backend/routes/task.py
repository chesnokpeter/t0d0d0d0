from fastapi import APIRouter, Security, Body
from datetime import date as datetype
from datetime import time as timetype
from t0d0d0d0.core.depends import uowdep
from t0d0d0d0.core.infra.db.models import TaskModel
from t0d0d0d0.core.infra.db.enums import TaskStatus
from t0d0d0d0.backend.answer import Answer, AnswerResModel
from t0d0d0d0.core.schemas.task import NewTaskSch, EditTaskSch
from t0d0d0d0.core.services.task import TaskService
from t0d0d0d0.core.depends import accessSecure, infra

taskRouter = APIRouter(prefix='/task', tags=['task'])

@taskRouter.post('/new/task', response_model=AnswerResModel[TaskModel]) 
async def new_task(data:NewTaskSch, uow=uowdep(infra()), credentials = Security(accessSecure)):
    s = await TaskService(uow).newTask(user_id=int(credentials["id"]), data=data)
    r = Answer.OkAnswerModel('task', 'task', data=s)
    return r.response

@taskRouter.get('/get/inbox', response_model=AnswerResModel[TaskModel]) 
async def get_inbox(uow=uowdep(infra()), credentials = Security(accessSecure)):
    s = await TaskService(uow).getInbox(user_id=int(credentials["id"]))
    r = Answer.OkAnswerModel('task', 'task', data=s)
    return r.response

@taskRouter.delete('/delete/task', response_model=AnswerResModel[None]) 
async def del_task(id:int = Body(embed=True), uow=uowdep(infra()), credentials = Security(accessSecure)):
    await TaskService(uow).delTask(user_id=int(credentials["id"]), id=id)
    r = Answer.OkAnswer('task', 'task', data=[{}])
    return r.response

@taskRouter.post('/get/taskByDate', response_model=AnswerResModel[TaskModel]) 
async def get_task_by_date(date:datetype = Body(embed=True), uow=uowdep(infra()), credentials = Security(accessSecure)):
    s = await TaskService(uow).getTaskByDate(user_id=int(credentials["id"]), date=date)
    r = Answer.OkAnswerModel('task', 'task', data=s)
    return r.response

@taskRouter.post('/get/taskById', response_model=AnswerResModel[TaskModel]) 
async def get_task_by_date(id:int = Body(embed=True), uow=uowdep(infra()), credentials = Security(accessSecure)):
    s = await TaskService(uow).getTaskById(user_id=int(credentials["id"]), id=id)
    r = Answer.OkAnswerModel('task', 'task', data=s)
    return r.response



@taskRouter.patch('/edit/name') 
async def edit_name(data:EditTaskSch[str], uow=uowdep(infra()), credentials = Security(accessSecure)):
    s = await TaskService(uow).editProperty(user_id=int(credentials["id"]), id=data.id, name=data.edit)
    r = Answer.OkAnswerModel('task', 'task', data=s)
    return r.response

@taskRouter.patch('/edit/date') 
async def edit_date(data:EditTaskSch[datetype], uow=uowdep(infra()), credentials = Security(accessSecure)):
    s = await TaskService(uow).editProperty(user_id=int(credentials["id"]), id=data.id, date=data.edit)
    r = Answer.OkAnswerModel('task', 'task', data=s)
    return r.response

@taskRouter.patch('/edit/time') 
async def edit_time(data:EditTaskSch[timetype], uow=uowdep(infra()), credentials = Security(accessSecure)):
    s = await TaskService(uow).editProperty(user_id=int(credentials["id"]), id=data.id, time=data.edit)
    r = Answer.OkAnswerModel('task', 'task', data=s)
    return r.response

@taskRouter.patch('/edit/status') 
async def edit_status(data:EditTaskSch[TaskStatus], uow=uowdep(infra()), credentials = Security(accessSecure)):
    s = await TaskService(uow).editProperty(user_id=int(credentials["id"]), id=data.id, status=data.edit)
    r = Answer.OkAnswerModel('task', 'task', data=s)
    return r.response

@taskRouter.patch('/edit/project') 
async def edit_project(data:EditTaskSch[int], uow=uowdep(infra()), credentials = Security(accessSecure)):
    s = await TaskService(uow).editProperty(user_id=int(credentials["id"]), id=data.id, project_id=data.edit)
    r = Answer.OkAnswerModel('task', 'task', data=s)
    return r.response
