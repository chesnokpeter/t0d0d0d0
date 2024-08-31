from typing import Type, TypeVar, Generic
from faststream.rabbit import RabbitBroker
import json

from t0d0d0d0.coreback.infra.broker.models import AbsModel, AuthnotifyModel

T = TypeVar('T', bound=AbsModel)

class AbsRepository:
    model: AbsModel
    def __init__(self): ...
    def get(self): raise NotImplementedError
    def add(self): raise NotImplementedError
    def delete(self): raise NotImplementedError

class Repository(Generic[T], AbsRepository):
    model: Type[T]
    def __init__(self, session: RabbitBroker):
        self.session = session
    async def send(self, data:str) -> None:
        await self.session.publish(data, 'authnotify')

class AuthnotifyRepository(Repository[AuthnotifyModel]):
    model = AuthnotifyModel