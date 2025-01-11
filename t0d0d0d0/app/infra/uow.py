from dataclasses import dataclass
from typing import TypeVar, Generic
from typing_extensions import Unpack
from asyncio import gather

from ..application.uses_cases import BaseUseCase
from .adapters import AbsConnector, AbsACIDConnector
from ..domain.repos.base import BaseRepo

T = TypeVar('T', bound=BaseUseCase)

class UnitOfWork(Generic[T]):
    uc: T
    def __init__(self, adapters: list[AbsConnector], use_case: T, repos: list[BaseRepo]=None):
        self.adapters = adapters
        self.uc = use_case
        self.depends_on = {use_case.repo_realizations[i].depends_on for i in use_case.repo_used} if not repos else {i.depends_on for i in repos}
        self.repos = repos if repos else None

    async def __aenter__(self) -> 'UnitOfWork[T]':
        for i in self.adapters:
            if i.__class__.__name__ in self.depends_on:
                await i.connect()
            else: 
                continue

            if self.repos:
                for j in self.repos:
                    if i.__class__.__name__ == j.depends_on:
                        j.connect(i.session)
            else:
                for j in self.uc.repo_used:
                    if i.__class__.__name__ == self.uc.repo_realizations[j].depends_on:
                        self.uc.repo_realizations[j].connect(i.session)

        return self

    async def __aexit__(self, *args):
        await gather(*(c.close() for c in self.adapters))

    async def commit(self):
        await gather(*(c.commit() for c in self.adapters if isinstance(c, AbsACIDConnector)))

    async def rollback(self):
        await gather(*(c.rollback() for c in self.adapters if isinstance(c, AbsACIDConnector)))


@dataclass(eq=False, slots=True)
class SetupUOW:
    adapters: list[AbsConnector]

    def uow(self, use_case: T) -> UnitOfWork[T]:
        return UnitOfWork[T](self.adapters, use_case)
    
    def uow_repos(self, use_case: T, *repos: Unpack[BaseRepo]) -> UnitOfWork[T]:
        return UnitOfWork[T](self.adapters, use_case, repos)



