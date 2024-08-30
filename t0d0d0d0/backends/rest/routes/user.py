from fastapi import APIRouter, Security, Depends, Body
from t0d0d0d0.core.inversion import uowdep
from t0d0d0d0.backends.rest.answer import Answer
from t0d0d0d0.core.schemas.user import SignUpSch
from t0d0d0d0.core.services.user import UserService
from t0d0d0d0.core.inversion import infra

from t0d0d0d0.backends.rest.depends import refreshSecure, access, refresh, accessSecure

userRouter = APIRouter(prefix='/user', tags=['user'])

@userRouter.post('/signup')
async def signup_user(data: SignUpSch, uow=uowdep(infra(memory=True))):
    s = await UserService(uow).signup(data)
    r = Answer.OkAnswer('user registered', 'user registered', [{}])
    access_token = access.create_access_token(subject={'id':s.id})
    refresh_token = refresh.create_refresh_token(subject={'id':s.id})
    access.set_access_cookie(r.response, access_token)
    refresh.set_refresh_cookie(r.response, refresh_token)
    return r.response

@userRouter.post('/login')
async def login_user(authcode:str = Body(embed=True), uow=uowdep(infra(memory=True))):
    payload = await UserService(uow).login(authcode)
    r = Answer.OkAnswer('user logged', 'user logged', [{}])
    access_token = access.create_access_token(subject={'id':payload.id})
    refresh_token = refresh.create_refresh_token(subject={'id':payload.id})
    access.set_access_cookie(r.response, access_token)
    refresh.set_refresh_cookie(r.response, refresh_token)
    return r.response   

@userRouter.get('/me') 
async def me_user(uow=uowdep(infra()), credentials = Security(accessSecure)):
    u = await UserService(uow).getOne(id=int(credentials["id"]))
    r = Answer.OkAnswerModel('user', 'user', data=u)
    return r.response

@userRouter.post('/refresh') 
async def refresh_token(uow=uowdep(infra()), credentials = Security(refreshSecure)):
    u = await UserService(uow).getOne(id=int(credentials["id"]))
    r = Answer.OkAnswer('access token has been updated', 'access token has been updated', data=[{}])
    access_token = access.create_access_token(subject={'id':credentials["id"]})
    access.set_access_cookie(r.response, access_token)
    return r.response

