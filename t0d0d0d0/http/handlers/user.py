from litestar import post
from litestar.di import Provide

from ...app.application import SignUpUseCase, SignInUseCase, GetByIdUseCase
from ..shortcuts import DishkaRouter, SUOW, UseCase, accessSecure, accST, refreshSecure, rshST

from ..schemas import SignUpSch


@post('/signup')
async def signup_user(data: SignUpSch, s: SUOW, uc: UseCase[SignUpUseCase], accessSecure: accST, refreshSecure: rshST) -> str:
    async with s.uow(uc) as uow:
        r, id = await uow.uc.execute(data)
        await uow.commit()
    token = accessSecure.encode(id)
    rtoken = refreshSecure.encode(id)
    r.add_cookie(access_token=token, refresh_token=rtoken)
    return r


@post('/login')
async def login_user(authcode: str, s: SUOW, uc: UseCase[SignInUseCase], accessSecure: accST, refreshSecure: rshST) -> str:
    async with s.uow(uc) as uow:
        r, id = await uow.uc.execute(authcode)
        await uow.commit()
    token = accessSecure.encode(id)
    rtoken = refreshSecure.encode(id)
    r.add_cookie(access_token=token, refresh_token=rtoken)
    return r


@get('/me')
async def me_user(uc: UseCase[GetByIdUseCase], s: SUOW):
    
    user = await UserService(uow).getOne(id=int(credentials['id']))
    response = Answer.OkAnswerModel('user', 'user', data=user)
    return response.response


@post('/refresh')
async def refresh_token(uow=Depends(uowdep(user)), credentials=Security(refreshSecure)):
    user = await UserService(uow).getOne(id=credentials['id'])
    response = Answer.OkAnswer(
        'access token has been updated',
        'access token has been updated',
        data=[{}],
    )
    access_token = access.create_access_token(subject={'id': credentials['id']})
    access.set_access_cookie(response.response, access_token)
    return response.response



router = DishkaRouter('/user', route_handlers=[
    signup_user,
    login_user
], dependencies={
    'accessSecure': Provide(lambda: accessSecure, use_cache=True),
    'refreshSecure': Provide(lambda: refreshSecure, use_cache=True)
})




# @post('/signup')
# async def signup_user(data: SignUpSch, uow=Depends(uowdep(user, authcode, task, project))):
#     user, private_key = await UserService(uow).signup(data)
#     response = Answer.OkAnswer('user registered', 'user registered', [{'private_key':private_key.decode()}])
#     access_token = access.create_access_token(subject={'id': user.id})
#     refresh_token = refresh.create_refresh_token(subject={'id': user.id})
#     access.set_access_cookie(response.response, access_token)
#     refresh.set_refresh_cookie(response.response, refresh_token)
#     return response.response


# @userRouter.post('/login')
# async def login_user(
#     authcode: str = Body(embed=True),
#     uow=Depends(uowdep(user, authcode, authnotify)),
# ):
#     payload, private_key = await UserService(uow).login(authcode)
#     response = Answer.OkAnswer('user logged', 'user logged', [{'private_key':private_key.decode()}])
#     access_token = access.create_access_token(subject={'id': payload.id})
#     refresh_token = refresh.create_refresh_token(subject={'id': payload.id})
#     access.set_access_cookie(response.response, access_token)
#     refresh.set_refresh_cookie(response.response, refresh_token)
#     return response.response


# @userRouter.get('/me')
# async def me_user(uow=Depends(uowdep(user)), credentials=Security(accessSecure)):
#     user = await UserService(uow).getOne(id=int(credentials['id']))
#     response = Answer.OkAnswerModel('user', 'user', data=user)
#     return response.response


# @userRouter.post('/refresh')
# async def refresh_token(uow=Depends(uowdep(user)), credentials=Security(refreshSecure)):
#     user = await UserService(uow).getOne(id=credentials['id'])
#     response = Answer.OkAnswer(
#         'access token has been updated',
#         'access token has been updated',
#         data=[{}],
#     )
#     access_token = access.create_access_token(subject={'id': credentials['id']})
#     access.set_access_cookie(response.response, access_token)
#     return response.response
