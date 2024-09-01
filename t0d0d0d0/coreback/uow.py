from abc import ABC, abstractmethod
from dataclasses import dataclass
from t0d0d0d0.coreback.infra.db.repositories import UserRepository, TaskRepository, ProjectRepository
from t0d0d0d0.coreback.infra.memory.repositories import AuthcodeRepository
from t0d0d0d0.coreback.infra.memory import get_async_conn_redis
from t0d0d0d0.coreback.infra.db import get_async_conn_postgres
from t0d0d0d0.coreback.infra.broker import get_async_conn_rabbit
from t0d0d0d0.coreback.infra.broker.repositories import AuthnotifyRepository, ShedulernotifyRepository
from t0d0d0d0.coreback.config import postgres_url, redis_host, redis_port, rabbit_url

from t0d0d0d0.coreback.infra.db.repositories import AbsRepository as DbAbsRepo
from t0d0d0d0.coreback.infra.memory.repositories import AbsRepository as MemoryAbsRepo
from t0d0d0d0.coreback.infra.broker.repositories import AbsRepository as BrokerAbsRepo

class AbsUnitOfWork(ABC):
    @abstractmethod
    def __init__(self): raise NotImplementedError
    @abstractmethod
    async def __aenter__(self): raise NotImplementedError
    @abstractmethod
    async def __aexit__(self): raise NotImplementedError
    @abstractmethod
    async def commit(self): raise NotImplementedError
    @abstractmethod
    async def rollback(self): raise NotImplementedError

@dataclass
class infra:
    db: bool = True
    memory: bool = False
    broker: bool = False

class UnitOfWork(AbsUnitOfWork):
    def __init__(self, infra:infra):
        self.infra = infra
        if self.infra.db:
            self.postgres_conn = get_async_conn_postgres(postgres_url)
        if self.infra.memory:
            self.redis_conn = get_async_conn_redis(redis_host=redis_host, redis_port=redis_port)
        if self.infra.broker:
            self.rabbit_conn = get_async_conn_rabbit(rabbit_url)

    async def __aenter__(self):
        self.user = DbAbsRepo()
        self.task = DbAbsRepo()
        self.project = DbAbsRepo()
        self.authcode = MemoryAbsRepo()
        self.authnotify = BrokerAbsRepo()
        self.sheduler = BrokerAbsRepo()
        if self.infra.db:
            self.session_postgres = self.postgres_conn()
            self.user = UserRepository(self.session_postgres)
            self.task = TaskRepository(self.session_postgres)
            self.project = ProjectRepository(self.session_postgres)
        if self.infra.memory:
            self.session_redis = await self.redis_conn()
            self.authcode = AuthcodeRepository(self.session_redis)
        if self.infra.broker:
            self.session_rabbit = self.rabbit_conn()
            await self.session_rabbit.connect()
            self.authnotify = AuthnotifyRepository(self.session_rabbit)
            self.sheduler = ShedulernotifyRepository(self.session_rabbit)

    async def __aexit__(self, *args):
        if self.infra.db:
            await self.rollback()
            await self.session_postgres.close()
        if self.infra.memory:
            self.session_redis.close()
        if self.infra.broker:
            await self.session_rabbit.close()

    async def commit(self):
        if self.infra.db:
            await self.session_postgres.commit()

    async def rollback(self):
        if self.infra.db:
            await self.session_postgres.rollback()