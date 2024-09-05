from fastapi import APIRouter, Security, Body, Depends
from datetime import date as datetype
from datetime import time as timetype
from t0d0d0d0.coreback.models.task import TaskModel, TaskStatus
from t0d0d0d0.restback.answer import Answer, AnswerResModel
from t0d0d0d0.coreback.schemas.task import NewTaskSch, EditTaskSch
from t0d0d0d0.coreback.services.task import TaskService
from t0d0d0d0.restback.depends import accessSecure, uowdep, \
    user, task, project, shedulernotify

taskRouter = APIRouter(prefix='/task', tags=['task'])

@taskRouter.post('/new', response_model=AnswerResModel[TaskModel]) 
async def new_task(data:NewTaskSch, uow=Depends(uowdep(user, task, project)), credentials = Security(accessSecure)):
    s = await TaskService(uow).new(user_id=int(credentials["id"]), data=data)
    r = Answer.OkAnswerModel('task', 'task', data=s)
    return r.response

@taskRouter.delete('/delete', response_model=AnswerResModel[None]) 
async def delete_task(id:int = Body(embed=True), uow=Depends(uowdep(user, task)), credentials = Security(accessSecure)):
    await TaskService(uow).delete(user_id=int(credentials["id"]), id=id)
    r = Answer.OkAnswer('task', 'task', data=[{}])
    return r.response

@taskRouter.post('/get/byDate', response_model=AnswerResModel[TaskModel]) 
async def get_task_by_date(date:datetype = Body(embed=True), uow=Depends(uowdep(user, task)), credentials = Security(accessSecure)):
    s = await TaskService(uow).getByDate(user_id=int(credentials["id"]), date=date)
    r = Answer.OkAnswerModel('task', 'task', data=s)
    return r.response

@taskRouter.post('/get/byId', response_model=AnswerResModel[TaskModel]) 
async def get_task_by_date(id:int = Body(embed=True), uow=Depends(uowdep(user, task)), credentials = Security(accessSecure)):
    s = await TaskService(uow).getById(user_id=int(credentials["id"]), id=id)
    r = Answer.OkAnswerModel('task', 'task', data=s)
    return r.response



@taskRouter.patch('/edit/name') 
async def edit_name(data:EditTaskSch[str], uow=Depends(uowdep(user, task, shedulernotify)), credentials = Security(accessSecure)):
    s = await TaskService(uow).edit(user_id=int(credentials["id"]), id=data.id, name=data.edit)
    r = Answer.OkAnswerModel('task', 'task', data=s)
    return r.response

@taskRouter.patch('/edit/date') 
async def edit_date(data:EditTaskSch[datetype], uow=Depends(uowdep(user, task, shedulernotify)), credentials = Security(accessSecure)):
    s = await TaskService(uow).edit(user_id=int(credentials["id"]), id=data.id, date=data.edit)
    r = Answer.OkAnswerModel('task', 'task', data=s)
    return r.response

@taskRouter.patch('/edit/time') 
async def edit_time(data:EditTaskSch[timetype], uow=Depends(uowdep(user, task, shedulernotify)), credentials = Security(accessSecure)):
    s = await TaskService(uow).edit(user_id=int(credentials["id"]), id=data.id, time=data.edit)
    r = Answer.OkAnswerModel('task', 'task', data=s)
    return r.response

@taskRouter.patch('/edit/status') 
async def edit_status(data:EditTaskSch[TaskStatus], uow=Depends(uowdep(user, task, shedulernotify)), credentials = Security(accessSecure)):
    s = await TaskService(uow).edit(user_id=int(credentials["id"]), id=data.id, status=data.edit)
    r = Answer.OkAnswerModel('task', 'task', data=s)
    return r.response

@taskRouter.patch('/edit/project') 
async def edit_project(data:EditTaskSch[int], uow=Depends(uowdep(user, task, shedulernotify)), credentials = Security(accessSecure)):
    s = await TaskService(uow).edit(user_id=int(credentials["id"]), id=data.id, project_id=data.edit)
    r = Answer.OkAnswerModel('task', 'task', data=s)
    return r.response



inboxRouter = APIRouter(prefix='/inbox', tags=['task'])

@inboxRouter.get('/get', response_model=AnswerResModel[TaskModel]) 
async def get_inbox(uow=Depends(uowdep(user, task)), credentials = Security(accessSecure)):
    s = await TaskService(uow).getInbox(user_id=int(credentials["id"]))
    r = Answer.OkAnswerModel('task', 'task', data=s)
    return r.response