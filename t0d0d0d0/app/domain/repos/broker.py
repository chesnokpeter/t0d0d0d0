from abc import ABC, abstractmethod

from ..interfaces import AbsBrokerMessage

class AbsBrokerRepo(ABC):

    @abstractmethod
    async def send(self, data: AbsBrokerMessage) -> None: raise NotImplementedError
