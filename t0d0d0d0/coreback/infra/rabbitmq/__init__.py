from typing import Callable
from faststream.rabbit import RabbitBroker
from t0d0d0d0.coreback.infra.abstract import AbsConnector

def get_async_conn_rabbit(rabbit_url: str) -> RabbitBroker:
    return lambda:RabbitBroker(rabbit_url)

class RabbitConnector(AbsConnector):
    def __init__(self, rabbit_url: str, connector_name: str = 'rabbit'):
        self.maker = get_async_conn_rabbit(rabbit_url)
        self.connector_name = connector_name
    async def connect(self):
        self._session = self.maker()
        await self._session.connect()
    async def commit(self):...
    async def rollback(self):...
    async def close(self):
        self._session.close()
    @property
    def session(self):
        return self._session