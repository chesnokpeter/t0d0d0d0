from litestar import post, get, patch, delete

from ...app.application import NewProjUseCase, AllProjectsUseCase, EditProjectUseCase, DeleteProjectUseCase
from ..shortcuts import DishkaRouter, SUOW, UseCase, FACCESS, RET

from ..schemas import NewProjectSch, EditProjectSch, DeleteProjectSch



@post('/new')
async def new_project(data: NewProjectSch, uc: UseCase[NewProjUseCase], s: SUOW, id: FACCESS) -> RET:
    async with s.uow(uc) as uow:
        r, model = await uow.uc.execute(id, data)
    return r


@get('/get')
async def get_user_projects(uc: UseCase[AllProjectsUseCase], s: SUOW, id: FACCESS) -> RET:
    async with s.uow(uc) as uow:
        r, model = await uow.uc.execute(id)
    return r



@patch('/edit/name')
async def edit_project(data: EditProjectSch, uc: UseCase[EditProjectUseCase], s: SUOW, id: FACCESS) -> RET:
    async with s.uow(uc) as uow:
        r, model = await uow.uc.execute(id, data.id, name=data.name)
    return r



@delete('/delete')
async def delete_project(data: DeleteProjectSch, uc: UseCase[DeleteProjectUseCase], s: SUOW, id: FACCESS) -> None:
    async with s.uow(uc) as uow:
        r = await uow.uc.execute(id, data.id)





router = DishkaRouter('/project', route_handlers=[
    new_project,
    get_user_projects,
    edit_project,
    delete_project
])

