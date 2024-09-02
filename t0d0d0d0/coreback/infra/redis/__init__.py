from typing import Callable
import asyncio_redis
from asyncio_redis import RedisProtocol


def get_async_conn_redis(redis_host: str, redis_port: int) -> Callable[[], RedisProtocol]:
    return lambda:asyncio_redis.Connection.create(host=redis_host, port=redis_port)
