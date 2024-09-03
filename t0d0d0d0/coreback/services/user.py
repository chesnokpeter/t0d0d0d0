from t0d0d0d0.coreback.services.abstract import AbsService

from t0d0d0d0.coreback.models.user import UserModel
from t0d0d0d0.coreback.models.authnotify import AuthnotifyModel
from t0d0d0d0.coreback.models.authcode import AuthcodeModel
from t0d0d0d0.coreback.schemas.user import NewUserSch
from t0d0d0d0.coreback.schemas.user import SignUpSch
from t0d0d0d0.coreback.uow import BaseUnitOfWork
from t0d0d0d0.coreback.exceptions import AuthException, AuthCodeException
from t0d0d0d0.coreback.utils import genAuthCode

class UserService(AbsService): 
    def __init__(self, uow: BaseUnitOfWork) -> None:
        self.uow = uow

    async def signup(self, data:SignUpSch) -> UserModel:
        """required: database, memory"""
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

    async def login(self, authcode:str) -> UserModel:
        """required: database, memory, broker"""
        async with self.uow:
            c = await self.uow.authcode.get(authcode)
            if not c:raise AuthCodeException('Authcode not found')
            await self.uow.authcode.delete(authcode)
            u = await self.uow.user.get_one(tgid=int(c.tgid))
            if not u: raise AuthException('User not found')
            await self.uow.authcode.delete(authcode)

            await self.uow.authnotify.send(AuthnotifyModel(tgid=u.tgid))

            return u.model()

    async def newAuthcode(self, tgid:int, tgusername: str) -> int:
        """required: memory"""
        async with self.uow:
            async def checkCode(code: str) -> str:
                check = await self.uow.authcode.get(code)
                if check:return await checkCode(genAuthCode())
                return code
            code = await checkCode(genAuthCode())
            await self.uow.authcode.add(code, AuthcodeModel(tgid=tgid, tgusername=tgusername))
            return code

    async def getOne(self, id:int) -> UserModel:
        """required: database"""
        async with self.uow:
            u = await self.uow.user.get_one(id=id)
            if not u: raise AuthException('User not found')
            return u.model()



    # async def checkIL(self, il: str) -> UserModel:
    #     async with self.uow:
    #         r = await self.uow.user.get_one(inviteLink=il)
    #         if not r: raise AuthILException('Invite link not found')
    #         return r.model()


        
        
    # async def getNewUserAuthcode(self, tgcode:str) -> AuthCodeModel:
    #     async with self.uow:
    #         model = await self.uow.cach.get(tgcode, json_load=True)
    #         if not model:raise AuthCodeException('Authcode not found')
    #         if isinstance(model, int): raise AuthCodeException('Authcode intended to a login')
    #         await self.uow.cach.delete(tgcode)
    #         return AuthCodeModel(**model) 

    # async def newAuthcode(self, tgid:int) -> int:
    #     async with self.uow:
    #         async def checkCode(code: str) -> str:
    #             check = await self.uow.cach.get(code)
    #             if check:return await checkCode(genAuthCode())
    #             return code
    #         code = await checkCode(genAuthCode())
    #         await self.uow.cach.add(code, tgid)
    #         return code
        
    # async def getAuthcode(self, tgcode:int) -> int:
    #     async with self.uow:
    #         model = await self.uow.cach.get(tgcode)
    #         if not model:raise AuthCodeException('Authcode not found')
    #         await self.uow.cach.delete(tgcode)
    #         return model
        