from typing import Type, TypeVar, Generic
from faststream.rabbit import RabbitBroker
import json

from t0d0d0d0.coreback.repos.abstract import BrokerAbsRepo, BrokerAbsModel

T = TypeVar('T', bound=BrokerAbsModel)

class RabbitmqDefaultRepo(Generic[T], BrokerAbsRepo):
    model: Type[T]
    def __init__(self, session: RabbitBroker):
        self.session = session
    async def send(self, data:T) -> None:
        print(json.dumps(data.model_dump()))
        await self.session.publish(json.dumps(data.model_dump(exclude=['queue_name'])), data.queue_name)
