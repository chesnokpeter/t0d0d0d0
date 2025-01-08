from abc import abstractmethod
from typing import Any
from ..interfaces import AbsMemoryMessage
from .base import BaseRepo, sT
from typing import Type, TypeVar

T = TypeVar('T', bound='AbsMemoryMessage')

class AbsMemoryRepo(BaseRepo[sT]):

    @abstractmethod
    async def add(self, key: Any, data: AbsMemoryMessage) -> AbsMemoryMessage: raise NotImplementedError

    @abstractmethod
    async def get(self, key: Any, ref: Type[T]) -> T | None: raise NotImplementedError

    @abstractmethod
    async def delete(self, key: Any) -> None: raise NotImplementedError


# from typing import TypeVar

# T = TypeVar('T')

# def add(a: Type[T], b: Type[T]) -> T:
#     return a + b

# result1 = add(AbsMemoryMessage, AbsMemoryMessage)        # result1 is of type int

# result2 = add("Hello, ", "World!")   # result2 is of type str
