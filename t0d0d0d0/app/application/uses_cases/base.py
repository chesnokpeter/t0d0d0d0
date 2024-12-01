from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Callable, Any

from ...presentation import Return
from ...domain.services import ConflictError, NotFoundError, IncorrectError, PermissionError

@dataclass(eq=False, slots=True)
class BaseUseCase(ABC):
    async def __call__(self, *args, **kwds) -> Return:
        return await self.execute(*args, **kwds)

    @abstractmethod
    async def execute(self, *args, **kwds) -> Return:raise NotImplementedError

    async def call_with_service_excepts(self, call: Callable[[], Any]) -> Return:
        try:
            r = await call()
        except (NotFoundError, ConflictError, IncorrectError, PermissionError) as service_error:
            r = Return.ErrAnswer(service_error.type, service_error.message)
        except Exception as e:
            raise e
        return r

