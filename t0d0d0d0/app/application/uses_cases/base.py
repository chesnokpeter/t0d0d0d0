from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Callable, Any, TypeVar, Awaitable, NewType

from ...presentation import ServiceReturn, SReturnBuilder
from ...domain.services import ConflictError, NotFoundError, IncorrectError, PermissionError

from ...domain.repos import BaseRepo

T = TypeVar('T')


RepoRealizations = NewType('RepoRealizations', dict[str, BaseRepo])

class UseCaseErrRet(Exception):
    def __init__(self, ret: ServiceReturn, *args):
        super().__init__(*args)
        self.ret = ret


@dataclass(eq=False)
class BaseUseCase(ABC):
    sret: SReturnBuilder
    repo_realizations: RepoRealizations

    service: Any = field(init=False)
    repo_used: list[BaseRepo] = field(init=False)

    async def __call__(self, *args, **kwds) -> ServiceReturn:
        return await self.execute(*args, **kwds)

    @abstractmethod
    async def execute(self, *args, **kwds) -> ServiceReturn :raise NotImplementedError

    async def call_with_service_excepts(self, call: Callable[[], Awaitable[T]]) -> T:
        try:
            r = await call()
        except (NotFoundError, ConflictError, IncorrectError, PermissionError) as service_error:
            raise UseCaseErrRet(ServiceReturn(service_error.type, service_error.message))
        except Exception as e:
            raise e
        return r

