from abc import ABC, abstractmethod
from typing import Any, TypeAlias

AbsModel: TypeAlias = Any

class MemoryAbsModel(ABC, AbsModel):
    memory_model_name: str
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.memory_model_name = cls.__name__
    @abstractmethod
    def model_dump(self): raise NotImplementedError

class BrokerAbsModel(ABC, AbsModel):
    queue_name: str
    @abstractmethod
    def model_dump(self): raise NotImplementedError

class DbAbsModel(ABC, AbsModel):
    id: int
    @abstractmethod
    def model_dump(self): raise NotImplementedError