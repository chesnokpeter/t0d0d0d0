from typing import Optional, Any
from asyncio_redis import RedisProtocol
from t0d0d0d0.core.infra.memory.models import MemoryModelManager, AuthCodeModel, Model

class MemoryController:
    def __init__(self, session: RedisProtocol):
        self.session = session
    async def get(self, key:str) -> Optional[Any]:
        data = await self.session.get(key)
        if data: return MemoryModelManager.deserialize(data)
        return data
    async def add(self, key:str, data:Model) -> None:
        return await self.session.set(key, MemoryModelManager.serialize(data))
    async def delete(self, key:str) -> None:
        await self.session.delete(keys=[key])


