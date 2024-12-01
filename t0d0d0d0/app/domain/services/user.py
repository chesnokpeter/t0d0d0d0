from dataclasses import dataclass

from datetime import date, datetime

from .exceptions import NotFoundError, ConflictError
from ..repos import AbsUserRepo, AbsEncryptionRepo, AbsProjectRepo, AbsTaskRepo, AbsBrokerRepo, AbsMemoryRepo
from ..models import UserModel
from ..entities import AddUser, AddProject, AddTask, AuthcodeMemory
from ..schemas import SignUpSch

@dataclass(eq=False, slots=True)
class UserService:
    user_repo: AbsUserRepo
    project_repo: AbsProjectRepo
    task_repo: AbsTaskRepo
    encryption_repo: AbsEncryptionRepo
    broker_repo: AbsBrokerRepo
    memory_repo: AbsMemoryRepo

    async def signup(self, data: SignUpSch) -> tuple[UserModel, bytes]: 
        reg = await self.memory_repo.get(data.authcode, AuthcodeMemory)
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
        return user, private_key_pem