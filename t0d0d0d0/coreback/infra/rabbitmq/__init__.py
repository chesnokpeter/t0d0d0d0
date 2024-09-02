from typing import Callable
from faststream.rabbit import RabbitBroker

def get_async_conn_rabbit(rabbit_url: str) -> RabbitBroker:
    return lambda:RabbitBroker(rabbit_url)