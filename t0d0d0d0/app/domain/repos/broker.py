from abc import abstractmethod

from ..interfaces import AbsBrokerMessage

from .base import BaseRepo, sT

class AbsBrokerRepo(BaseRepo[sT]):

    @abstractmethod
    async def send(self, data: AbsBrokerMessage) -> None: raise NotImplementedError
