from faststream.rabbit import RabbitBroker
from typing import Callable
from .base import AbsConnector


def get_async_conn_rabbit(rabbit_url: str) -> Callable[[], RabbitBroker]:
    return lambda: RabbitBroker(rabbit_url)





class RabbitConnector(AbsConnector[Callable[[], Callable[[], RabbitBroker]]]):
    async def connect(self):
        self._session: RabbitBroker = self.maker()
        await self._session.connect()

    async def close(self):
        if self._session:
            await self._session.close()

    @property
    def session(self):
        return self._session


