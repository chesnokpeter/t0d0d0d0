from typing import Callable
import asyncio_redis
from asyncio_redis import RedisProtocol
from .base import AbsConnector


def get_async_conn_redis(redis_host: str, redis_port: int) -> Callable[[], RedisProtocol]:
    return lambda: asyncio_redis.Connection.create(host=redis_host, port=redis_port)


class RedisConnector(AbsConnector[Callable[[], Callable[[], RedisProtocol]]]):
    async def connect(self):
        self._session: RedisProtocol = await self.maker()

    async def close(self):
        if self._session:
            self._session.close()

    @property
    def session(self):
        return self._session


