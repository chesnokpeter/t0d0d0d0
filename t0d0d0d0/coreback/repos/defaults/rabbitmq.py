from typing import Type, TypeVar, Generic
from faststream.rabbit import RabbitBroker
import json

from t0d0d0d0.coreback.repos.abstract import BrokerAbsRepo, BrokerAbsModel

T = TypeVar('T', bound=BrokerAbsModel)

class RabbitmqDefaultRepo(Generic[T], BrokerAbsRepo[RabbitBroker]):
    model: Type[T]
    async def send(self, data:T) -> None:
        await self.session.publish(json.dumps(data.model_dump(exclude=['queue_name'])), data.queue_name)

