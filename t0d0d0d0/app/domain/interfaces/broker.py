from abc import ABC, abstractmethod

class AbsBrokerMessage(ABC):
    @property
    @abstractmethod
    def queue_name(self): raise NotImplementedError

    def dict(self):
        return {field: getattr(self, field) for field in self.__annotations__}
