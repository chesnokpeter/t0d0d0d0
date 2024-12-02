from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Callable, Any

from ...presentation import ServiceReturn
from ...domain.services import ConflictError, NotFoundError, IncorrectError, PermissionError

@dataclass(eq=False, slots=True)
class BaseUseCase(ABC):
    async def __call__(self, *args, **kwds) -> ServiceReturn:
        return await self.execute(*args, **kwds)

    @abstractmethod
    async def execute(self, *args, **kwds) -> ServiceReturn:raise NotImplementedError

    async def call_with_service_excepts(self, call: Callable[[], Any]) -> ServiceReturn:
        try:
            r = await call()
        except (NotFoundError, ConflictError, IncorrectError, PermissionError) as service_error:
            r = ServiceReturn.ErrAnswer(service_error.type, service_error.message)
        except Exception as e:
            raise e
        return r

