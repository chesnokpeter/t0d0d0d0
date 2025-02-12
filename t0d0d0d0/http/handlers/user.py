from litestar import post, get

from ...app.application import SignUpUseCase, SignInUseCase, GetByIdUseCase
from ..shortcuts import DishkaRouter, SUOW, UseCase, accST, rshST, FACCESS, RET, FREFRESH

from ..schemas import SignUpSch, SignInSch


@post('/signup')
async def signup_user(data: SignUpSch, s: SUOW, uc: UseCase[SignUpUseCase], accessSecure: accST, refreshSecure: rshST) -> RET:
    async with s.uow(uc) as uow:
        r, id = await uow.uc.execute(data)
        await uow.commit()
    token = accessSecure.encode(id)
    rtoken = refreshSecure.encode(id)
    r.add_cookie(access_token=token, refresh_token=rtoken)
    return r


@post('/login')
async def login_user(data: SignInSch, s: SUOW, uc: UseCase[SignInUseCase], accessSecure: accST, refreshSecure: rshST) -> RET:
    async with s.uow(uc) as uow:
        r, id = await uow.uc.execute(data.authcode)
        await uow.commit()
    token = accessSecure.encode(id)
    rtoken = refreshSecure.encode(id)
    r.add_cookie(access_token=token, refresh_token=rtoken)
    return r


@get('/me')
async def me_user(uc: UseCase[GetByIdUseCase], s: SUOW, id: FACCESS) -> RET:
    async with s.uow(uc) as uow:
        r, model = await uow.uc.execute(id)
    return r


@post('/refresh')
async def refresh_token(uc: UseCase[GetByIdUseCase], s: SUOW, accessSecure: accST, refreshSecure: rshST, id: FREFRESH) -> RET:
    async with s.uow(uc) as uow:
        r, model = await uow.uc.execute(id)
    token = accessSecure.encode(id)
    rtoken = refreshSecure.encode(id)
    r.add_cookie(access_token=token, refresh_token=rtoken)
    return r



router = DishkaRouter('/user', route_handlers=[
    signup_user,
    login_user,
    me_user,
    refresh_token
])




