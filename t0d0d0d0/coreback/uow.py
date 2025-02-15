from abc import ABC, abstractmethod
from functools import wraps
from asyncio import gather
from typing import ParamSpecArgs

from t0d0d0d0.coreback.exceptions import NoAccessForRepo, NoConnectorForRepo
from t0d0d0d0.coreback.infra.abstract import AbsConnector
from t0d0d0d0.coreback.repos.abstract import AbsRepo
from t0d0d0d0.coreback.repos.authcode import AuthcodeRepo
from t0d0d0d0.coreback.repos.authnotify import AuthnotifyRepo
from t0d0d0d0.coreback.repos.project import ProjectRepo
from t0d0d0d0.coreback.repos.shedulernotify import ShedulernotifyRepo
from t0d0d0d0.coreback.repos.task import TaskRepo
from t0d0d0d0.coreback.repos.tasknotify import TasknotifyRepo
from t0d0d0d0.coreback.repos.user import UserRepo
from t0d0d0d0.coreback.state import Repos


class AbsUnitOfWork(ABC):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class UnitOfWork(AbsUnitOfWork):
    def __init__(self, repos: list[AbsRepo], connectors: list[AbsConnector]):
        self.connectors = connectors
        self.repo_names = [repo.reponame for repo in repos]
        [setattr(self, repo.reponame, repo) for repo in repos]
        for r in repos:
            if r.require_connector not in {c.connector_name for c in connectors}:
                raise NoConnectorForRepo(f'No Connector For Repo "{r.reponame}"')

    async def __aenter__(self):
        for c in self.connectors:
            await c.connect()
            for repo_name in self.repo_names:
                repo: AbsRepo = getattr(self, repo_name)
                if repo.require_connector == c.connector_name:
                    repo(c.session)

        return self

    async def __aexit__(self, *args):
        await gather(*(c.close() for c in self.connectors))

    async def commit(self):
        await gather(*(c.commit() for c in self.connectors))

    async def rollback(self):
        await gather(*(c.rollback() for c in self.connectors))


class ALLRepoUnitOfWork(AbsUnitOfWork, ABC):
    user: UserRepo
    task: TaskRepo
    project: ProjectRepo
    authcode: AuthcodeRepo
    authnotify: AuthnotifyRepo
    shedulernotify: ShedulernotifyRepo
    tasknotify: TasknotifyRepo


class AbsService:
    uow: UnitOfWork


def uowaccess(*access: Repos):
    """this decorator checks access to repositories inside a unit of work"""

    def decorator(func):
        @wraps(func)
        async def wrapper(self: AbsService, *args, **kwargs):
            for i in access:
                if not getattr(self.uow, i.value, False):
                    raise NoAccessForRepo(f'No Access For Repo "{i}"')
            return await func(self, *args, **kwargs)

        return wrapper

    return decorator
