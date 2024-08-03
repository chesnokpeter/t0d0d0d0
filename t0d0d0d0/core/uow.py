from t0d0d0d0.core.infra.db.controllers import UserController, TaskController, ProjectController
from t0d0d0d0.core.infra.memory import get_async_conn_redis
from t0d0d0d0.core.infra.memory.controller import MemoryController
from t0d0d0d0.core.infra.db import asyncfactory_postgres
from abc import ABC, abstractmethod
from dataclasses import dataclass
from t0d0d0d0.core.config import postgres_url, redis_host, redis_port

class AbsUnitOfWork(ABC):
    @abstractmethod
    def __init__(self): raise NotImplementedError
    @abstractmethod
    async def __aenter__(self): raise NotImplementedError
    @abstractmethod
    async def __aexit__(self, *args): raise NotImplementedError
    @abstractmethod
    async def commit(self): raise NotImplementedError
    @abstractmethod
    async def rollback(self): raise NotImplementedError

@dataclass
class infra:
    db: bool = True
    memory: bool = False

class UnitOfWork:
    def __init__(self, infra:infra):
        self.infra = infra
        if self.infra.db:
            self.session_factory = asyncfactory_postgres(postgres_url)
        if self.infra.memory:
            self.redis_conn = get_async_conn_redis

    async def __aenter__(self):
        if self.infra.db:
            self.session_postgres = self.session_factory()
            self.user = UserController(self.session_postgres)
            self.task = TaskController(self.session_postgres)
            self.project = ProjectController(self.session_postgres)
        if self.infra.memory:
            self.session_redis = await self.redis_conn(redis_host=redis_host, redis_port=redis_port)
            self.session_redis = await self.session_redis()
            self.memory = MemoryController(self.session_redis)

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