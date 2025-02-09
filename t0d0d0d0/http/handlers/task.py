from litestar import post, get, patch, delete, Router
from datetime import datetime, time
from ...app.application import NewTaskUseCase, DeleteTaskUseCase, TaskByDateUseCase, TaskByIdUseCase, EditTaskUseCase, AllInboxUseCase
from ...app.shared import TaskStatus
from ..shortcuts import DishkaRouter, SUOW, UseCase, FACCESS, RET

from ..schemas import EditTaskSch, NewTaskSch, DeleteTaskSch, GetTasksByDate, GetTasksById, EditTaskSch


@post('/new')
async def new_task(data: NewTaskSch, uc: UseCase[NewTaskUseCase], s: SUOW, id: FACCESS) -> RET:
    async with s.uow(uc) as uow:
        r, model = await uow.uc.execute(id, data)
    return r

@delete('/delete')
async def delete_task(data: DeleteTaskSch, uc: UseCase[DeleteTaskUseCase], s: SUOW, id: FACCESS) -> RET:
    async with s.uow(uc) as uow:
        r = await uow.uc.execute(id, data)
    return r

@post('/get/byDate')
async def get_tasks_by_date(data: GetTasksByDate, uc: UseCase[TaskByDateUseCase], s: SUOW, id: FACCESS) -> RET:
    async with s.uow(uc) as uow:
        r, model = await uow.uc.execute(id, data.date)
    return r


@post('/get/byId')
async def get_tasks_by_id(data: GetTasksById, uc: UseCase[TaskByIdUseCase], s: SUOW, id: FACCESS) -> RET:
    async with s.uow(uc) as uow:
        r, model = await uow.uc.execute(id, data.id)
    return r


@patch('/edit/name')
async def task_edit_name(data: EditTaskSch[str], uc: UseCase[EditTaskUseCase], s: SUOW, id: FACCESS) -> RET:
    async with s.uow(uc) as uow:
        r, model = await uow.uc.execute(id, data.id, name=data.edit)
    return r


@patch('/edit/date')
async def task_edit_date(data: EditTaskSch[datetime], uc: UseCase[EditTaskUseCase], s: SUOW, id: FACCESS) -> RET:
    async with s.uow(uc) as uow:
        r, model = await uow.uc.execute(id, data.id, date=data.edit)
    return r



@patch('/edit/time')
async def task_edit_time(data: EditTaskSch[time], uc: UseCase[EditTaskUseCase], s: SUOW, id: FACCESS) -> RET:
    async with s.uow(uc) as uow:
        r, model = await uow.uc.execute(id, data.id, time=data.edit)
    return r



@patch('/edit/status')
async def task_edit_status(data: EditTaskSch[TaskStatus], uc: UseCase[EditTaskUseCase], s: SUOW, id: FACCESS) -> RET:
    async with s.uow(uc) as uow:
        r, model = await uow.uc.execute(id, data.id, status=data.edit)
    return r

@patch('/edit/project')
async def task_edit_project(data: EditTaskSch[int], uc: UseCase[EditTaskUseCase], s: SUOW, id: FACCESS) -> RET:
    async with s.uow(uc) as uow:
        r, model = await uow.uc.execute(id, data.id, project_id=data.edit)
    return r




@get('/get')
async def get_inbox(uc: UseCase[AllInboxUseCase], s: SUOW, id: FACCESS) -> RET:
    async with s.uow(uc) as uow:
        r, model = await uow.uc.execute(id)
    return r


router = Router('/inbox', route_handlers=[
    get_inbox,
])



router = DishkaRouter('/task', route_handlers=[
    router,
    new_task,
    delete_task,
    get_tasks_by_date,
    get_tasks_by_id,
    task_edit_name,
    task_edit_project,
    task_edit_date,
    task_edit_status,
    task_edit_time,
])