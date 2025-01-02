from abc import abstractmethod

from ..interfaces import AbsBrokerMessage

from .base import BaseRepo, TSESION

class AbsBrokerRepo(BaseRepo[TSESION]):

    @abstractmethod
    async def send(self, data: AbsBrokerMessage) -> None: raise NotImplementedError
