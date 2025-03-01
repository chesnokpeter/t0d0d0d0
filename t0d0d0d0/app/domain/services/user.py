from dataclasses import dataclass

from datetime import date, datetime

from .exceptions import NotFoundError, ConflictError
from ..models import UserModel
from ..entities import AddUser, AddProject, AddTask, AuthcodeMemory, AuthnotifyBroker, EmptyMemory
from ..schemas import SignUpSch
from ..repos import AbsUserRepo, AbsEncryptionRepo, AbsProjectRepo, AbsTaskRepo, AbsBrokerRepo, AbsMemoryRepo

from .utils import genAuthCode

@dataclass(eq=False, slots=True)
class UserService:
    user_repo: AbsUserRepo
    project_repo: AbsProjectRepo
    task_repo: AbsTaskRepo
    encryption_repo: AbsEncryptionRepo
    broker_repo: AbsBrokerRepo
    memory_repo: AbsMemoryRepo

    async def signup(self, data: SignUpSch) -> tuple[UserModel, bytes, int]: 
        reg: AuthcodeMemory = await self.memory_repo.get(key=data.authcode, ref=AuthcodeMemory)
        if not reg:
            raise NotFoundError('authcode not found')

        private_key, public_key = self.encryption_repo.rsa_keys()
        private_key_pem = self.encryption_repo.rsa_private_serial(private_key)
        public_key_pem = self.encryption_repo.rsa_public_serial(public_key)
        aes_private_key  = self.encryption_repo.aes_encrypt(private_key_pem.decode(), self.encryption_repo.convert_tgid_to_aes_key(reg.tgid))

        name = self.encryption_repo.rsa_encrypt(data.name, public_key)
        tgid = self.encryption_repo.hashed(str(reg.tgid))
        tgusername = self.encryption_repo.rsa_encrypt(reg.tgusername, public_key)

        exist = await self.user_repo.get_all(tgid=tgid)
        if exist:
            raise ConflictError('user already exist')
        exist = await self.user_repo.get_all(tgusername=tgusername)
        if exist:
            raise ConflictError('user already exist')

        user = AddUser(
            tgid=tgid,
            tgusername=tgusername,
            name=name,
            aes_private_key=aes_private_key,
            public_key=public_key_pem,
            notify_id=reg.tgid
        )
        user = await self.user_repo.add(user)
        project = AddProject(
            name=self.encryption_repo.rsa_encrypt('first project', public_key), 
            user_id=user.id
        )
        project = await self.project_repo.add(project)
        task = AddTask(
            name=self.encryption_repo.rsa_encrypt('an in inbox!', public_key),
            user_id=user.id
        )
        task = await self.task_repo.add(task)
        task = AddTask(
            name=self.encryption_repo.rsa_encrypt('today task!', public_key),
            date=date.today(), 
            time=datetime.now().time(),
            project_id=project.id,
            user_id=user.id
        )
        task = await self.task_repo.add(task)

        await self.memory_repo.delete(data.authcode)
        return user, private_key_pem, user.id


    async def login(self, authcode: str) -> tuple[UserModel, bytes, int]: 
        login: AuthcodeMemory = await self.memory_repo.get(authcode, AuthcodeMemory)
        if not login:
            raise NotFoundError('authcode not found')

        user = await self.user_repo.get_all(tgid=self.encryption_repo.hashed(str(login.tgid)))
        if not user:
            raise NotFoundError('user not found')
        user = user[0]

        await self.broker_repo.send(AuthnotifyBroker(tgid=login.tgid))
        private_key = self.encryption_repo.aes_decrypt(user.aes_private_key, self.encryption_repo.convert_tgid_to_aes_key(login.tgid))
        await self.memory_repo.delete(authcode)
        return user, private_key, user.id

    async def test(self, user_id: int) -> UserModel | None:
        u = await self.user_repo.get(user_id)
        return u


    async def prereg(self, tgid: int, tgusername: str) -> str:
        async def checkCode(code: str) -> str:
            check: AuthcodeMemory = await self.memory_repo.get(code, AuthcodeMemory)
            if check:
                return await checkCode(genAuthCode())
            return code
        
        # exist = await self.user_repo.get_all(tgid=self.encryption_repo.hashed(str(tgid)))
        # if exist:
        #     raise ConflictError('user already exist')
        # exist = await self.user_repo.get_all(tgusername=self.encryption_repo.hashed(tgusername))
        # if exist:
        #     raise ConflictError('user already exist')

        code = await checkCode(genAuthCode())
        await self.memory_repo.add(code, AuthcodeMemory(tgid=tgid, tgusername=tgusername))
        return code


    async def get_by_id(self, id: int) -> UserModel:
        u = await self.user_repo.get(id)
        if not u:
            raise NotFoundError('user not found')
        return u


    async def get_by_tgid(self, tgid: int) -> UserModel:
        u = await self.user_repo.get_all(tgid=tgid)
        if not u:
            raise NotFoundError('user not found')
        return u[0]
    
    async def get_by_tgid_not_excep(self, tgid: int) -> UserModel | None:
        u = await self.user_repo.get_all(tgid=tgid)
        return u[0] if u else None
    



    async def gen_new_authcode(self) -> str:
        async def checkCode(code: str) -> str:
            check: AuthcodeMemory = await self.memory_repo.get(code, AuthcodeMemory)
            if check:
                return await checkCode(genAuthCode())
            check: EmptyMemory = await self.memory_repo.get(code, EmptyMemory)
            if check:
                return await checkCode(genAuthCode())
            return code

        code = await checkCode(genAuthCode())
        await self.memory_repo.add(code, EmptyMemory())
        return code


    async def check_authcode(self, code: str) -> AuthcodeMemory:
        check: AuthcodeMemory = await self.memory_repo.get(code, AuthcodeMemory)

        if check:
            return check

        raise NotFoundError('authcode not found')

    async def login_authcode(self, code: str) -> tuple[UserModel, bytes, int]:
        check: AuthcodeMemory = await self.memory_repo.get(code, AuthcodeMemory)

        if check:
            user = await self.user_repo.get_all(tgid=self.encryption_repo.hashed(str(check.tgid)))
            if not user:
                return await self.signup_authcode(code)
            user = user[0]
            await self.broker_repo.send(AuthnotifyBroker(tgid=check.tgid))
            private_key = self.encryption_repo.aes_decrypt(user.aes_private_key, self.encryption_repo.convert_tgid_to_aes_key(check.tgid))
            await self.memory_repo.delete(code)
            return user, private_key, user.id

        raise NotFoundError('authcode not found')

    async def signup_authcode(self, code: str) -> tuple[UserModel, bytes, int]: 
        reg: AuthcodeMemory = await self.memory_repo.get(code, ref=AuthcodeMemory)
        if not reg:
            raise NotFoundError('authcode not found')

        private_key, public_key = self.encryption_repo.rsa_keys()
        private_key_pem = self.encryption_repo.rsa_private_serial(private_key)
        public_key_pem = self.encryption_repo.rsa_public_serial(public_key)
        aes_private_key  = self.encryption_repo.aes_encrypt(private_key_pem.decode(), self.encryption_repo.convert_tgid_to_aes_key(reg.tgid))

        name = self.encryption_repo.rsa_encrypt(reg.tgusername, public_key)
        tgid = self.encryption_repo.hashed(str(reg.tgid))
        tgusername = self.encryption_repo.rsa_encrypt(reg.tgusername, public_key)

        exist = await self.user_repo.get_all(tgid=tgid)
        if exist:
            return await self.login_authcode(code)
        exist = await self.user_repo.get_all(tgusername=tgusername)
        if exist:
            return await self.login_authcode(code)

        user = AddUser(
            tgid=tgid,
            tgusername=tgusername,
            name=name,
            aes_private_key=aes_private_key,
            public_key=public_key_pem,
            notify_id=reg.tgid
        )
        user = await self.user_repo.add(user)
        project = AddProject(
            name=self.encryption_repo.rsa_encrypt('first project', public_key), 
            user_id=user.id
        )
        project = await self.project_repo.add(project)
        task = AddTask(
            name=self.encryption_repo.rsa_encrypt('an in inbox!', public_key),
            user_id=user.id
        )
        task = await self.task_repo.add(task)
        task = AddTask(
            name=self.encryption_repo.rsa_encrypt('today task!', public_key),
            date=date.today(), 
            time=datetime.now().time(),
            project_id=project.id,
            user_id=user.id
        )
        task = await self.task_repo.add(task)

        await self.memory_repo.delete(code)
        return user, private_key_pem, user.id


    async def update_authcode(self, authcode: str, tgid: int, tgusername: str) -> str:
        # exist = await self.user_repo.get_all(tgid=self.encryption_repo.hashed(str(tgid)))
        # if exist:
        #     raise ConflictError('user already exist')
        # exist = await self.user_repo.get_all(tgusername=self.encryption_repo.hashed(tgusername))
        # if exist:
        #     raise ConflictError('user already exist')

        await self.memory_repo.add(authcode, AuthcodeMemory(tgid=tgid, tgusername=tgusername))
        return authcode