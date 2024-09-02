from typing import Type, TypeVar, Generic
from faststream.rabbit import RabbitBroker
import json

from t0d0d0d0.coreback.infra.broker.models import AbsModel, AuthnotifyModel, TasknotifyModel, ShedulernotifyModel

class AbsRepo:
    model: AbsModel
    def __init__(self): ...
    def send(self): raise NotImplementedError

T = TypeVar('T', bound=AbsModel)


class Repo(Generic[T], AbsRepo):
    model: Type[T]
    def __init__(self, session: RabbitBroker):
        self.session = session
    async def send(self, data:T) -> None:
        print(json.dumps(data.model_dump()))
        await self.session.publish(json.dumps(data.model_dump(exclude=['queue_name'])), data.queue_name)

class AuthnotifyRepo(Repo[AuthnotifyModel]):
    model = AuthnotifyModel

class TasknotifyRepo(Repo[TasknotifyModel]):
    model = TasknotifyModel

class ShedulernotifyRepo(Repo[ShedulernotifyModel]):
    model = ShedulernotifyModel