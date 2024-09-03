from abc import ABC, abstractmethod

from t0d0d0d0.coreback.infra.abstract import AbsConnector
from t0d0d0d0.coreback.repos.abstract import AbsRepo, DbAbsRepo, MemoryAbsRepo, BrokerAbsRepo
from t0d0d0d0.coreback.repos.authcode import AuthcodeRepo
from t0d0d0d0.coreback.repos.authnotify import AuthnotifyRepo
from t0d0d0d0.coreback.repos.project import ProjectRepo
from t0d0d0d0.coreback.repos.user import UserRepo
from t0d0d0d0.coreback.repos.task import TaskRepo
from t0d0d0d0.coreback.repos.shedulernotify import ShedulernotifyRepo
from t0d0d0d0.coreback.repos.tasknotify import TasknotifyRepo
from t0d0d0d0.coreback.exceptions import NoConnectorForRepo


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


class UnitOfWork(AbsUnitOfWork):
    def __init__(self, connectors: list[AbsConnector], repos: list[AbsRepo]):
        self.connectors = connectors
        self.repos_names = [repo.reponame for repo in repos]
        [setattr(self, repo.reponame, repo) for repo in repos]
        for r in repos:
            if r.require_connector not in {c.connector_name for c in connectors}:
                raise NoConnectorForRepo(f'No Connector For Repo \"{r.reponame}\"')

    async def __aenter__(self):
        for repo_name in self.repos_names:
            repo: AbsRepo = getattr(self, repo_name)
            for c in self.connectors:
                if repo.require_connector == c.connector_name:
                    await c.connect()
                    repo(c.session)

    async def __aexit__(self, *args):
        [await c.close() for c in self.connectors]

    async def commit(self, *args):
        [await c.commit() for c in self.connectors]
    
    async def rollback(self):
        [await c.rollback() for c in self.connectors]


class BaseUnitOfWork(AbsUnitOfWork, ABC):
    user = UserRepo
    task = TaskRepo
    project = ProjectRepo
    authcode = AuthcodeRepo
    authnotify = AuthnotifyRepo
    shedulernotify = ShedulernotifyRepo
    tasknotify = TasknotifyRepo