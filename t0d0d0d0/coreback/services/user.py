from typing import Annotated, TypeAlias

from t0d0d0d0.coreback.exceptions import UserException
from t0d0d0d0.coreback.models.authcode import AuthcodeModel
from t0d0d0d0.coreback.models.authnotify import AuthnotifyModel
from t0d0d0d0.coreback.models.user import UserModel
from t0d0d0d0.coreback.schemas.project import NewProjectSch
from t0d0d0d0.coreback.schemas.task import NewTaskSch
from t0d0d0d0.coreback.schemas.user import NewUserSch, SignUpSch
from t0d0d0d0.coreback.services.abstract import AbsService
from t0d0d0d0.coreback.uow import BaseUnitOfWork, UnitOfWork, uowaccess
from t0d0d0d0.coreback.utils import genAuthCode, rsa_generate_keys, aes_decrypt

from datetime import date, datetime

UnitOfWork: TypeAlias = Annotated[BaseUnitOfWork, UnitOfWork]



class UserService(AbsService):
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    @uowaccess('user', 'project', 'task', 'authcode')
    async def signup(self, data: SignUpSch) -> UserModel: #! ADD SECURITY AES RSA
        async with self.uow:
            c = await self.uow.authcode.get(data.authcode)
            if not c:
                raise UserException('authcode not found')

            u = await self.uow.user.get(tgid=c.tgid)
            if u:
                raise UserException('user already exist')
            u = await self.uow.user.get(tgusername=c.tgusername)
            if u:
                raise UserException('user already exist')

            private_key, public_key = rsa_generate_keys()
            aes_private_key  = aes_decrypt(private_key, )

            u = NewUserSch(tgid=c.tgid, tgusername=c.tgusername, name=data.name)
            u = await self.uow.user.add(**u.model_dump())
            p = await self.uow.project.add(name='first project', user_id=u.id)
            await self.uow.task.add(name='an in inbox!', user_id=u.id)
            await self.uow.task.add(name='today task!', date=date.today(), time=datetime.now().time(), project_id=p.id, user_id=u.id)
            await self.uow.commit()
            await self.uow.authcode.delete(data.authcode)
            return u.model()

    @uowaccess('user', 'authcode', 'authnotify')
    async def login(self, authcode: str) -> UserModel: #! ADD SECURITY AES RSA
        async with self.uow:
            c = await self.uow.authcode.get(authcode)
            if not c:
                raise UserException('authcode not found')

            await self.uow.authcode.delete(authcode)
            u = await self.uow.user.get_one(tgid=int(c.tgid))
            if not u:
                raise UserException('user not found')

            await self.uow.authcode.delete(authcode)
            await self.uow.authnotify.send(AuthnotifyModel(tgid=u.tgid))
            return u.model()

    @uowaccess('authcode')
    async def newAuthcode(self, tgid: int, tgusername: str) -> int:
        async with self.uow:

            async def checkCode(code: str) -> str:
                check = await self.uow.authcode.get(code)
                if check:
                    return await checkCode(genAuthCode())
                return code

            code = await checkCode(genAuthCode())
            await self.uow.authcode.add(code, AuthcodeModel(tgid=tgid, tgusername=tgusername))
            return code

    @uowaccess('user')
    async def getOne(self, id: int) -> UserModel:
        async with self.uow:
            u = await self.uow.user.get_one(id=id)
            if not u:
                raise UserException('user not found')
            return u.model()


    @uowaccess('user')
    async def getfromTG(self, tgid: int) -> UserModel:
        async with self.uow:
            u = await self.uow.user.get_one(tgid=tgid)
            if not u:
                raise UserException('user not found')
            return u.model()