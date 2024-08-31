from abc import ABC, abstractmethod
from pydantic import BaseModel

class AbsModel(ABC):
    queue_name: str
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.queue_name = cls.__name__
    @abstractmethod
    def model_dump(self): raise NotImplementedError

class AuthnotifyModel(BaseModel, AbsModel):
    tgid: int