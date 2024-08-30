from abc import ABC, abstractmethod
from typing import Type, TypeVar, Generic
from asyncio_redis import RedisProtocol
import json

from t0d0d0d0.core.infra.memory.models import AuthcodeModel, AbsModel

T = TypeVar('T', bound=AbsModel)

class AbsRepository(ABC):
    model: AbsModel
    def __init__(self): ...
    @abstractmethod
    def get(self): raise NotImplementedError
    @abstractmethod
    def add(self): raise NotImplementedError
    @abstractmethod
    def delete(self): raise NotImplementedError

class Repository(Generic[T], AbsRepository):
    model: Type[T]
    def __init__(self, session: RedisProtocol):
        self.session = session
    async def get(self, key:str) -> T | None:
        data = await self.session.get(key)
        if not data: return None
        data = json.loads(data)
        memory_model_name = data.pop("memory_model_name", None)
        if memory_model_name != self.model.__name__:return None
        return self.model(**data)
    async def add(self, key:str, data:T) -> None:
        await self.session.set(key, json.dumps(data.model_dump()))
    async def delete(self, key:str) -> None:
        await self.session.delete(keys=[key])

class AuthcodeRepository(Repository[AuthcodeModel]):
    model = AuthcodeModel