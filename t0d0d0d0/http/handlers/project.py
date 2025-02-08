from litestar import post, get

from ...app.application import NewProjUseCase
from ..shortcuts import DishkaRouter, SUOW, UseCase, accST, rshST, FACCESS, RET, FREFRESH

from ..schemas import NewProjectSch


@post('/new')
async def new_project(
    data: NewProjectSch,
    uow = Depends(uowdep(user, project)),
    credentials = Security(accessSecure),
):
    s = await ProjectService(uow).new(user_id=int(credentials['id']), data=data)
    r = Answer.OkAnswerModel('project', 'project', data=s, encrypted=['name'])
    return r.response


@get('/new')
async def new_project(data: NewProjectSch, uc: UseCase[NewProjUseCase], s: SUOW, id: FACCESS) -> RET:
    async with s.uow(uc) as uow:
        r, model = await uow.uc.execute(id)
    return r



@get('/get')
async def get_user_projects(uow=Depends(uowdep(user, project)), credentials=Security(accessSecure)):
    s = await ProjectService(uow).getAll(user_id=int(credentials['id']))
    r = Answer.OkAnswerModel('project', 'project', data=s, encrypted=['name'])
    return r.response


@patch('/edit/name')
async def edit_project(
    id: int = Body(embed=True),
    name: str = Body(embed=True),
    uow=Depends(uowdep(user, project)),
    credentials=Security(accessSecure),
):
    await ProjectService(uow).edit(user_id=int(credentials['id']), project_id=id, name=name)
    r = Answer.OkAnswer('project', 'project', data=[{}])
    return r.response


@delete('/delete')
async def delete_project(
    id: int = Body(embed=True),
    uow=Depends(uowdep(user, project)),
    credentials=Security(accessSecure),
):
    await ProjectService(uow).delete(user_id=int(credentials['id']), project_id=id)
    r = Answer.OkAnswer('project', 'project', data=[{}])
    return r.response



router = DishkaRouter('/project', route_handlers=[


])

