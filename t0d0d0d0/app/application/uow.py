from abc import ABC, abstractmethod

class AbsUnitOfWork(ABC):
    @abstractmethod
    def __init__(self): raise NotImplementedError

    @abstractmethod
    async def __aenter__(self) -> 'AbsUnitOfWork': raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, *args): raise NotImplementedError

    @abstractmethod
    async def commit(self): raise NotImplementedError

    @abstractmethod
    async def rollback(self): raise NotImplementedError
