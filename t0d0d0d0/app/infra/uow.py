from dataclasses import dataclass, field
from typing import Type, TypeVar, Generic
from asyncio import gather

from ..application.uses_cases import BaseUseCase
from .adapters import AbsConnector, AbsACIDConnector


T = TypeVar('T', bound=BaseUseCase)

class UnitOfWork(Generic[T]):
    uc: T
    def __init__(self, adapters: list[AbsConnector], use_case: T):
        self.adapters = adapters
        self.uc = use_case
        self.depends_on = {use_case.repo_realizations[i].depends_on for i in use_case.repo_used}

    async def __aenter__(self) -> 'UnitOfWork[T]':
        for i in self.adapters:
            if i.__class__.__name__ in self.depends_on:
                await i.connect()
            else: 
                continue

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
    


