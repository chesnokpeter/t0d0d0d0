from abc import ABC, abstractmethod
from typing import TypeVar, Callable, TypeAlias, Generic

T = TypeVar('T')

ConnMaker: TypeAlias = Callable[[], T]

class AbsConnector(ABC, Generic[T]):
    _session = None
    maker: ConnMaker[T]

    def __init__(self, maker: ConnMaker[T]):
        self.maker = maker()

    @abstractmethod
    async def connect(self): raise NotImplementedError

    @abstractmethod
    async def close(self): raise NotImplementedError

    @property
    @abstractmethod
    def session(self) -> T: raise NotImplementedError


class AbsACIDConnector(AbsConnector[T]):
    @abstractmethod
    async def commit(self): raise NotImplementedError

    @abstractmethod
    async def rollback(self): raise NotImplementedError



