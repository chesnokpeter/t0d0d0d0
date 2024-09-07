import json
from typing import Generic, Type, TypeVar

from faststream.rabbit import RabbitBroker

from t0d0d0d0.coreback.repos.abstract import BrokerAbsModel, BrokerAbsRepo

T = TypeVar('T', bound=BrokerAbsModel)


class RabbitmqDefaultRepo(Generic[T], BrokerAbsRepo[RabbitBroker]):
    model: Type[T]

    def __init__(self, require_connector: str = 'rabbit'):
        self.require_connector = require_connector

    async def send(self, data: T) -> None:
        await self.session.publish(
            json.dumps(data.model_dump(exclude=['queue_name'])), data.queue_name
        )
