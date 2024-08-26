from typing import Optional
from t0d0d0d0.core.infra.db.models import NewUserModel, UserModel
from t0d0d0d0.core.infra.memory.models import AuthCodeModel
from t0d0d0d0.core.schemas.user import SignUpSch
from t0d0d0d0.core.uow import  UnitOfWork
from t0d0d0d0.core.exceptions import AuthException, AuthCodeException
from t0d0d0d0.core.utils import genAuthCode

class UserService: 
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def signup(self, data:SignUpSch) -> int:
        """required: database, memory"""
        async with self.uow:
            c: Optional[AuthCodeModel] = await self.uow.memory.get(data.authcode)
            if not c: raise AuthCodeException('Authcode not found')

            u = await self.uow.user.get(tgid=c.tgid)
            if u: raise AuthException('User already exist')
            u = await self.uow.user.get(tgusername=c.tgusername)
            if u: raise AuthException('User already exist')

            newuser = NewUserModel(tgid=c.tgid, tgusername=c.tgusername, name=data.name)
            user = await self.uow.user.add(**newuser.model_dump())
            await self.uow.commit()
            await self.uow.memory.delete(data.authcode)
            return user.id

    async def login(self, authcode:str) -> int:
        """required: database, memory"""
        async with self.uow:
            c:Optional[AuthCodeModel] = await self.uow.memory.get(authcode)
            if not c:raise AuthCodeException('Authcode not found')
            await self.uow.memory.delete(authcode)
            u = await self.uow.user.get_one(tgid=int(c.tgid))
            if not u: raise AuthException('User not found')
            await self.uow.memory.delete(authcode)
            return u.model().id

    async def newAuthcode(self, tgid:int, tgusername: str) -> int:
        """required: memory"""
        async with self.uow:
            async def checkCode(code: str) -> str:
                check = await self.uow.memory.get(code)
                if check:return await checkCode(genAuthCode())
                return code
            code = await checkCode(genAuthCode())
            await self.uow.memory.add(code, AuthCodeModel(tgid=tgid, tgusername=tgusername))
            return code

    async def getUser(self, id:int) -> UserModel:
        """required: database"""
        async with self.uow:
            u = await self.uow.user.get_one(id=id)
            if not u: raise AuthException('User not found')
            return UserModel(**u.model().model_dump())



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
        