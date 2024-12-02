from abc import ABC, abstractmethod

from ..interfaces import AbsBrokerMessage

from .base import BaseRepo

class AbsBrokerRepo(BaseRepo, ABC):

    @abstractmethod
    async def send(self, data: AbsBrokerMessage) -> None: raise NotImplementedError
