from dataclasses import dataclass

from datetime import datetime

from .exceptions import NotFoundError, ConflictError
from ..interfaces import AbsBrokerMessage
from ..models import TaskModel, TaskModelWithProjName
from ..entities import AddTask, AuthnotifyBroker
from ..schemas import NewTaskSch
from ..repos import AbsUserRepo, AbsEncryptionRepo, AbsProjectRepo, AbsTaskRepo, AbsBrokerRepo, AbsMemoryRepo

from ...shared import dtcls_slots2dict

@dataclass(eq=False, slots=True)
class TaskService:
    user_repo: AbsUserRepo
    project_repo: AbsProjectRepo
    task_repo: AbsTaskRepo
    encryption_repo: AbsEncryptionRepo
    broker_repo: AbsBrokerRepo
    memory_repo: AbsMemoryRepo


    async def new(self, user_id: int, data: NewTaskSch) -> TaskModel:
        u = await self.user_repo.get(user_id)
        if not u:
            raise NotFoundError('user not found')

        if data.project_id:
            p = await self.project_repo.get(data.project_id)
            if not p:
                raise NotFoundError('project not found')

        name = self.encryption_repo.rsa_encrypt(data.name, self.encryption_repo.rsa_public_deserial(u.public_key))
        data = dtcls_slots2dict(data)
        data['name'] = name
        p = AddTask(**data, user_id=user_id)
        return await self.task_repo.add(p)


    async def get_inbox(self, user_id: int) -> list[TaskModel] | None:
        u = await self.user_repo.get(user_id)
        if not u:
            raise NotFoundError('user not found')

        return await self.task_repo.get_all(user_id=user_id, project_id=None, date=None, time=None)


    async def get_all(self, user_id: int) -> list[TaskModelWithProjName] | None:
        u = await self.user_repo.get(user_id)
        if not u:
            raise NotFoundError('user not found')

        return await self.task_repo.get_all_with_proj_name(user_id)


    async def get_by_id(self, user_id: int, id: int) -> TaskModel:
        u = await self.user_repo.get(user_id)
        if not u:
            raise NotFoundError('user not found')

        t = await self.task_repo.get(id)
        if not t:
            raise NotFoundError('task not found')
        if t.user_id != user_id:
            raise NotFoundError('task not found')
        return t



    async def edit(self, user_id: int, id: int, **data) -> TaskModel:
        u = await self.user_repo.get(user_id)
        if not u:
            raise NotFoundError('user not found')

        t = await self.task_repo.get(id)
        if not t:
            raise NotFoundError('task not found')
        if t.user_id != user_id:
            raise NotFoundError('task not found')
        
        data['user_id'] = user_id

        if data.get('name'):
            if data['name'] == '':
                data['name'] = ' '
            data['name'] = self.encryption_repo.rsa_encrypt(data['name'], self.encryption_repo.rsa_public_deserial(u.public_key))

        upd = await self.task_repo.update(id, AddTask(**data))

        if data.get('time', None):
            combined_datetime = datetime.combine(t.date, t.time)
            now = datetime.now()
            delaydelta = combined_datetime - now
            delay = delaydelta.total_seconds()
            if delay > 0:
                pr = self.encryption_repo.rsa_private_deserial(self.encryption_repo.aes_decrypt(u.aes_private_key, self.encryption_repo.convert_tgid_to_aes_key(u.notify_id)))
                taskname = self.encryption_repo.rsa_decrypt(t.name, pr)
                projname = self.encryption_repo.rsa_decrypt(upd.project_name, pr)
                tasknotify = self.broker_repo.send() TasknotifyModel(tgid=u.notify_id, taskname=taskname, projname=projname)
                sheduler = ShedulernotifyModel(
                    queue_after_delay=tasknotify.queue_name,
                    delay=round(delay),
                    message=tasknotify.model_dump_json(),
                )
                await self.uow.shedulernotify.send(sheduler)

        return upd


    async def delete(self, user_id: int, id: int) -> None:
        u = await self.user_repo.get(user_id)
        if not u:
            raise NotFoundError('user not found')

        t = await self.task_repo.get(id)
        if not t:
            raise NotFoundError('task not found')
        if t.user_id != user_id:
            raise NotFoundError('task not found')

        await self.task_repo.delete(id)



    async def get_by_date(self, user_id: int, date: datetime) -> list[TaskModelWithProjName] | None:
        u = await self.user_repo.get(user_id)
        if not u:
            raise NotFoundError('user not found')

        return await self.task_repo.get_all_with_proj_name(user_id=user_id, date=date)