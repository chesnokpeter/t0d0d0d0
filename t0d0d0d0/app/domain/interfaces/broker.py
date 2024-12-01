from abc import ABC, abstractmethod

class AbsBrokerMessage(ABC):
    @property
    @abstractmethod
    def queue_name(self): raise NotImplementedError

    @abstractmethod
    def dict(self): raise NotImplementedError
