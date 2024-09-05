from fastapi import APIRouter, Security, Depends, Body
from t0d0d0d0.restback.answer import Answer
from t0d0d0d0.coreback.schemas.user import SignUpSch
from t0d0d0d0.coreback.services.user import UserService

from t0d0d0d0.restback.depends import refreshSecure, access, refresh, accessSecure, uowdep, \
    user, authcode, authnotify

userRouter = APIRouter(prefix="/user", tags=["user"])

@userRouter.post("/signup")
async def signup_user(data: SignUpSch, uow=Depends(uowdep(user, authcode))):

    user = await UserService(uow).signup(data)
    response = Answer.OkAnswer("user registered", "user registered", [{}])
    access_token = access.create_access_token(subject={"id": user.id})
    refresh_token = refresh.create_refresh_token(subject={"id": user.id})
    access.set_access_cookie(response.response, access_token)
    refresh.set_refresh_cookie(response.response, refresh_token)
    return response.response


@userRouter.post("/login")
async def login_user(authcode: str = Body(embed=True), uow=Depends(uowdep(user, authcode, authnotify))):

    payload = await UserService(uow).login(authcode)
    response = Answer.OkAnswer("user logged", "user logged", [{}])
    access_token = access.create_access_token(subject={"id": payload.id})
    refresh_token = refresh.create_refresh_token(subject={"id": payload.id})
    access.set_access_cookie(response.response, access_token)
    refresh.set_refresh_cookie(response.response, refresh_token)
    return response.response


@userRouter.get("/me")
async def me_user(uow=Depends(uowdep(user)), credentials=Security(accessSecure)):

    user = await UserService(uow).getOne(id=int(credentials["id"]))
    response = Answer.OkAnswerModel("user", "user", data=user)
    return response.response


@userRouter.post("/refresh")
async def refresh_token(uow=Depends(uowdep(user)), credentials=Security(refreshSecure)):

    user = await UserService(uow).getOne(id=credentials["id"])
    response = Answer.OkAnswer("access token has been updated", "access token has been updated", data=[{}])
    access_token = access.create_access_token(subject={"id": credentials["id"]})
    access.set_access_cookie(response.response, access_token)
    return response.response
