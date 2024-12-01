from abc import ABC, abstractmethod
from typing import Any
from ..interfaces import AbsMemoryMessage

from typing import Type, TypeVar

T = TypeVar('T', bound=AbsMemoryMessage)

class AbsMemoryRepo(ABC):

    @abstractmethod
    async def add(self, data: AbsMemoryMessage) -> AbsMemoryMessage: raise NotImplementedError

    @abstractmethod
    async def get(self, key: Any, ref: Type[T]) -> T | None: raise NotImplementedError

    @abstractmethod
    async def delete(self, key: Any) -> None: raise NotImplementedError


