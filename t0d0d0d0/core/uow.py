from abc import ABC, abstractmethod
from dataclasses import dataclass
from t0d0d0d0.core.infra.db.repositories import UserRepository, TaskRepository, ProjectRepository
from t0d0d0d0.core.infra.memory import get_async_conn_redis
from t0d0d0d0.core.infra.memory.repositories import AuthcodeRepository
from t0d0d0d0.core.infra.db import get_async_conn_postgres
from t0d0d0d0.core.config import postgres_url, redis_host, redis_port

from t0d0d0d0.core.infra.db.repositories import AbsRepository as DbAbsRepo
from t0d0d0d0.core.infra.memory.repositories import AbsRepository as MemoryAbsRepo

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

class UnitOfWork(AbsUnitOfWork):
    def __init__(self, infra:infra):
        self.infra = infra
        if self.infra.db:
            self.postgres_conn = get_async_conn_postgres(postgres_url)
        if self.infra.memory:
            self.redis_conn = get_async_conn_redis(redis_host=redis_host, redis_port=redis_port)

    async def __aenter__(self):
        self.user = DbAbsRepo
        self.task = DbAbsRepo
        self.project = DbAbsRepo
        self.authcode = MemoryAbsRepo
        if self.infra.db:
            self.session_postgres = self.postgres_conn()
            self.user = UserRepository(self.session_postgres)
            self.task = TaskRepository(self.session_postgres)
            self.project = ProjectRepository(self.session_postgres)
        if self.infra.memory:
            self.session_redis = await self.redis_conn()
            self.authcode = AuthcodeRepository(self.session_redis)

    async def __aexit__(self, *args):
        if self.infra.db:
            await self.rollback()
            await self.session_postgres.close()
        if self.infra.memory:
            self.session_redis.close()

    async def commit(self):
        if self.infra.db:
            await self.session_postgres.commit()

    async def rollback(self):
        if self.infra.db:
            await self.session_postgres.rollback()