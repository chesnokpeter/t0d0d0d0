from faststream.rabbit import RabbitBroker
from typing import Callable


def get_async_conn_rabbit(rabbit_url: str) -> Callable[[], RabbitBroker]:
    return lambda: RabbitBroker(rabbit_url)

