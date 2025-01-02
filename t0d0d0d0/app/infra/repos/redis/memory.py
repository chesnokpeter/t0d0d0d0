import json
from typing import Type
from ....domain.repos import AbsMemoryRepo
from ....domain.repos.memory import AbsMemoryMessage, T

from asyncio_redis import RedisProtocol


class MemoryRepoRedis(AbsMemoryRepo[RedisProtocol]):
    async def get(self, key: str, ref: Type[T]) -> T | None:
        data = await self.session.get(key)  # type: ignore
        if not data:
            return None
        data = json.loads(data)
        memory_model_name = data.pop('memory_model_name', None)
        if memory_model_name != ref.__name__:
            return None
        return ref(**data)

    async def add(self, key: str, data: AbsMemoryMessage) -> None:
        await self.session.set(key, json.dumps(data.model_dump()))  # type: ignore

    async def delete(self, key: str) -> None:
        await self.session.delete(keys=[key])  # type: ignore







