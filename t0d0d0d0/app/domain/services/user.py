from dataclasses import dataclass

from ..repos import AbsUserRepo, AbsEncryptionRepo, AbsProjectRepo, AbsTaskRepo
from ..models import UserModel
from ..entities import AddUser

@dataclass(slots=True)
class UserService:
    user_repo: AbsUserRepo
    project_repo: AbsProjectRepo
    task_repo: AbsTaskRepo
    encryption_repo: AbsEncryptionRepo

    async def signup(self, data: AddUser) -> tuple[UserModel, bytes]: 
        self.user_repo.add(data)

        # async with self.uow:
        #     c = await self.uow.authcode.get(data.authcode)
        #     if not c:
        #         raise UserException('authcode not found')

        #     private_key, public_key = rsa_keys()
        #     private_key_pem = rsa_private_serial(private_key)
        #     public_key_pem = rsa_public_serial(public_key)
        #     aes_private_key  = aes_encrypt(private_key_pem.decode(), convert_tgid_to_aes_key(c.tgid))

        #     name = rsa_encrypt(data.name, public_key)
        #     tgid = hashed(str(c.tgid))
        #     tgusername = rsa_encrypt(c.tgusername, public_key)

        #     u = await self.uow.user.get(tgid=tgid)
        #     if u:
        #         raise UserException('user already exist')
        #     u = await self.uow.user.get(tgusername=tgusername)
        #     if u:
        #         raise UserException('user already exist')

        #     u = await self.uow.user.add(name=name, tgid=tgid, tgusername=tgusername, aes_private_key=aes_private_key, public_key=public_key_pem, notify_id=c.tgid)
        #     p = await self.uow.project.add(name=rsa_encrypt('first project', public_key), user_id=u.id)
        #     await self.uow.task.add(name=rsa_encrypt('an in inbox!', public_key=public_key), user_id=u.id)
        #     await self.uow.task.add(name=rsa_encrypt('today task!', public_key=public_key), date=date.today(), time=datetime.now().time(), project_id=p.id, user_id=u.id)
        #     await self.uow.commit()
        #     await self.uow.authcode.delete(data.authcode)
        #     return u.model(), private_key_pem