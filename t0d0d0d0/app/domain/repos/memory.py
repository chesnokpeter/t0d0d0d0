from abc import abstractmethod
from typing import Any
from ..interfaces import AbsMemoryMessage
from .base import BaseRepo, TSESION
from typing import Type, TypeVar

T = TypeVar('T', bound=AbsMemoryMessage)

class AbsMemoryRepo(BaseRepo[TSESION]):

    @abstractmethod
    async def add(self, key: Any, data: AbsMemoryMessage) -> AbsMemoryMessage: raise NotImplementedError

    @abstractmethod
    async def get(self, key: Any, ref: Type[T]) -> T | None: raise NotImplementedError

    @abstractmethod
    async def delete(self, key: Any) -> None: raise NotImplementedError


