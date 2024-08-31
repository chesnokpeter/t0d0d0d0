from abc import ABC, abstractmethod
from pydantic import BaseModel

class AbsModel(ABC):
    memory_model_name: str
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.memory_model_name = cls.__name__
    @abstractmethod
    def model_dump(self): raise NotImplementedError


class AuthcodeModel(BaseModel, AbsModel):
    tgid: int
    tgusername: str

