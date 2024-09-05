from t0d0d0d0.coreback.services.abstract import AbsService
from t0d0d0d0.coreback.models.user import UserModel
from t0d0d0d0.coreback.models.authnotify import AuthnotifyModel
from t0d0d0d0.coreback.models.authcode import AuthcodeModel
from t0d0d0d0.coreback.schemas.user import NewUserSch
from t0d0d0d0.coreback.schemas.user import SignUpSch
from t0d0d0d0.coreback.uow import BaseUnitOfWork, UnitOfWork, uowaccess
from t0d0d0d0.coreback.exceptions import AuthException, AuthCodeException
from t0d0d0d0.coreback.utils import genAuthCode

from typing import Annotated, TypeAlias

UnitOfWork: TypeAlias = Annotated[BaseUnitOfWork, UnitOfWork]

class UserService(AbsService): 
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    @uowaccess('user', 'authcode')
    async def signup(self, data:SignUpSch) -> UserModel:
        async with self.uow:
            c = await self.uow.authcode.get(data.authcode)
            if not c: raise AuthCodeException('Authcode not found')

            u = await self.uow.user.get(tgid=c.tgid)
            if u: raise AuthException('User already exist')
            u = await self.uow.user.get(tgusername=c.tgusername)
            if u: raise AuthException('User already exist')

            u = NewUserSch(tgid=c.tgid, tgusername=c.tgusername, name=data.name)
            u = await self.uow.user.add(**u.model_dump())
            await self.uow.commit()
            await self.uow.authcode.delete(data.authcode)
            return u.model()

    @uowaccess('user', 'authcode', 'authnotify')
    async def login(self, authcode:str) -> UserModel:
        async with self.uow:
            c = await self.uow.authcode.get(authcode)
            if not c:raise AuthCodeException('Authcode not found')
            await self.uow.authcode.delete(authcode)
            u = await self.uow.user.get_one(tgid=int(c.tgid))
            if not u: raise AuthException('User not found')
            await self.uow.authcode.delete(authcode)
            await self.uow.authnotify.send(AuthnotifyModel(tgid=u.tgid))
            return u.model()

    @uowaccess('authcode')
    async def newAuthcode(self, tgid:int, tgusername: str) -> int:
        async with self.uow:
            async def checkCode(code: str) -> str:
                check = await self.uow.authcode.get(code)
                if check:return await checkCode(genAuthCode())
                return code
            code = await checkCode(genAuthCode())
            await self.uow.authcode.add(code, AuthcodeModel(tgid=tgid, tgusername=tgusername))
            return code

    @uowaccess('user')
    async def getOne(self, id:int) -> UserModel:
        async with self.uow:
            u = await self.uow.user.get_one(id=id)
            if not u: raise AuthException('User not found')
            return u.model()

    # @uowaccess('task')
    # async def test(self) -> UserModel:
    #     async with self.uow:
    #         u = await self.uow.task.get()
    #         a = await self.uow.user.get()
    #         # await self.uow.commit()
    #         # return u.model()
