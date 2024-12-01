from dataclasses import dataclass

from ..repos import AbsUserRepo, AbsEncryptionRepo, AbsProjectRepo, AbsTaskRepo, AbsBrokerRepo, AbsMemoryRepo
from ..models import UserModel
from ..entities import AddUser, AddProject, AddTask, AuthcodeMemory
from .exceptions import NotFoundError, ConflictError
from ..schemas import SignUp

@dataclass(eq=False, slots=True)
class UserService:
    user_repo: AbsUserRepo
    project_repo: AbsProjectRepo
    task_repo: AbsTaskRepo
    encryption_repo: AbsEncryptionRepo
    broker_repo: AbsBrokerRepo
    memory_repo: AbsMemoryRepo

    async def signup(self, data: SignUp) -> tuple[UserModel, bytes]: 
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

        user = AddUser(tgid=tgid, tgusername=tgusername, name=name, aes_private_key=aes_private_key, public_key=public_key_pem, notify_id=reg.tgid)
        project = AddProject(name=self.encryption_repo.rsa_encrypt('first project'))

        u = await self.uow.user.add(name=name, tgid=tgid, tgusername=tgusername, aes_private_key=aes_private_key, public_key=public_key_pem, notify_id=c.tgid)
        p = await self.uow.project.add(name=rsa_encrypt('first project', public_key), user_id=u.id)
        await self.uow.task.add(name=rsa_encrypt('an in inbox!', public_key=public_key), user_id=u.id)
        await self.uow.task.add(name=rsa_encrypt('today task!', public_key=public_key), date=date.today(), time=datetime.now().time(), project_id=p.id, user_id=u.id)
        await self.uow.commit()
        await self.uow.authcode.delete(data.authcode)
        return u.model(), private_key_pem