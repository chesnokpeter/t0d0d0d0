from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any
from t0d0d0d0.coreback.infra.db.repositories import UserRepo, TaskRepo, ProjectRepo
from t0d0d0d0.coreback.infra.memory.repositories import AuthcodeRepo
from t0d0d0d0.coreback.infra.memory import get_async_conn_redis
from t0d0d0d0.coreback.infra.db import get_async_conn_postgres
from t0d0d0d0.coreback.infra.broker import get_async_conn_rabbit
from t0d0d0d0.coreback.infra.broker.repositories import AuthnotifyRepo, ShedulernotifyRepo
from t0d0d0d0.coreback.config import postgres_url, redis_host, redis_port, rabbit_url

from t0d0d0d0.coreback.infra.db.repositories import AbsRepo as DbAbsRepo
from t0d0d0d0.coreback.infra.memory.repositories import AbsRepo as MemoryAbsRepo
from t0d0d0d0.coreback.infra.broker.repositories import AbsRepo as BrokerAbsRepo

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
            self.user = UserRepo(self.session_postgres)
            self.task = TaskRepo(self.session_postgres)
            self.project = ProjectRepo(self.session_postgres)
        if self.infra.memory:
            self.session_redis = await self.redis_conn()
            self.authcode = AuthcodeRepo(self.session_redis)
        if self.infra.broker:
            self.session_rabbit = self.rabbit_conn()
            await self.session_rabbit.connect()
            self.authnotify = AuthnotifyRepo(self.session_rabbit)
            self.sheduler = ShedulernotifyRepo(self.session_rabbit)

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


from t0d0d0d0.coreback.infra.abstract import AbsConnector
from t0d0d0d0.coreback.repos.abstract import AbsRepo
from t0d0d0d0.coreback.exceptions import NoConnectorForRepo

class UnitOfWork:
    def __init__(self, connectors: list[AbsConnector], repos: list[AbsRepo]):
        self.connectors = connectors
        self.repos_names = [repo.reponame for repo in repos]
        [setattr(self, repo.reponame, repo) for repo in repos]
        for r in repos:
            if r.require_connector not in {c.connector_name for c in connectors}:
                raise NoConnectorForRepo(f'No Connector For Repo "{r.reponame}"')

    async def __aenter__(self):
        for repo_name in self.repos_names:
            repo: AbsRepo = getattr(self, repo_name)
            for c in self.connectors:
                if repo.require_connector == c.connector_name:
                    session = await c.connect()
                    await repo.__call__(session)

