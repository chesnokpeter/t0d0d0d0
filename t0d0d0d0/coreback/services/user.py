from t0d0d0d0.coreback.exceptions import UserException
from t0d0d0d0.coreback.models.authcode import AuthcodeModel
from t0d0d0d0.coreback.models.authnotify import AuthnotifyModel
from t0d0d0d0.coreback.models.user import UserModel
from t0d0d0d0.coreback.schemas.user import SignUpSch
from t0d0d0d0.coreback.services.abstract import AbsService
from t0d0d0d0.coreback.uow import uowaccess
from t0d0d0d0.coreback.utils import genAuthCode, convert_tgid_to_aes_key
from t0d0d0d0.coreback.encryption import aes_decrypt, aes_encrypt, rsa_keys, rsa_encrypt, rsa_private_serial, rsa_public_serial, hashed
from t0d0d0d0.coreback.state import Repos

from datetime import date, datetime



class UserService(AbsService):
    @uowaccess(Repos.USER, Repos.PROJECT, Repos.TASK, Repos.AUTHCODE)
    async def signup(self, data: SignUpSch) -> tuple[UserModel, bytes]: 
        async with self.uow:
            c = await self.uow.authcode.get(data.authcode)
            if not c:
                raise UserException('authcode not found')

            private_key, public_key = rsa_keys()
            private_key_pem = rsa_private_serial(private_key)
            public_key_pem = rsa_public_serial(public_key)
            aes_private_key  = aes_encrypt(private_key_pem.decode(), convert_tgid_to_aes_key(c.tgid))

            name = rsa_encrypt(data.name, public_key)
            tgid = hashed(str(c.tgid))
            tgusername = rsa_encrypt(c.tgusername, public_key)

            u = await self.uow.user.get(tgid=tgid)
            if u:
                raise UserException('user already exist')
            u = await self.uow.user.get(tgusername=tgusername)
            if u:
                raise UserException('user already exist')

            u = await self.uow.user.add(name=name, tgid=tgid, tgusername=tgusername, aes_private_key=aes_private_key, public_key=public_key_pem, notify_id=c.tgid)
            p = await self.uow.project.add(name=rsa_encrypt('first project', public_key), user_id=u.id)
            await self.uow.task.add(name=rsa_encrypt('an in inbox!', public_key=public_key), user_id=u.id)
            await self.uow.task.add(name=rsa_encrypt('today task!', public_key=public_key), date=date.today(), time=datetime.now().time(), project_id=p.id, user_id=u.id)
            await self.uow.commit()
            await self.uow.authcode.delete(data.authcode)
            return u.model(), private_key_pem

    @uowaccess(Repos.USER, Repos.AUTHCODE, Repos.AUTHNOTIFY)
    async def login(self, authcode: str) -> tuple[UserModel, bytes]: 
        async with self.uow:
            c = await self.uow.authcode.get(authcode)
            if not c:
                raise UserException('authcode not found')
            await self.uow.authcode.delete(authcode)
            u = await self.uow.user.get_one(tgid=hashed(str(c.tgid)))
            if not u:
                raise UserException('user not found')
            await self.uow.authnotify.send(AuthnotifyModel(tgid=c.tgid))
            private_key = aes_decrypt(u.aes_private_key, convert_tgid_to_aes_key(c.tgid))
            return u.model(), private_key

    @uowaccess(Repos.AUTHCODE)
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

    @uowaccess(Repos.USER)
    async def getOne(self, id: int) -> UserModel:
        async with self.uow:
            u = await self.uow.user.get_one(id=id)
            if not u:
                raise UserException('user not found')
            return u.model()


    @uowaccess(Repos.USER)
    async def getfromTG(self, tgid: int) -> UserModel:
        async with self.uow:
            u = await self.uow.user.get_one(tgid=tgid)
            if not u:
                raise UserException('user not found')
            return u.model()