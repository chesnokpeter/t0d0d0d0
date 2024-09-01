from abc import ABC, abstractmethod
from pydantic import BaseModel

class AbsModel(ABC):
    queue_name: str
    @abstractmethod
    def model_dump(self): raise NotImplementedError

class AuthnotifyModel(BaseModel, AbsModel):
    queue_name: str = 'notifyauth'
    tgid: int

class TasknotifyModel(BaseModel, AbsModel):
    queue_name: str = 'notifytask'
    tgid: int
    taskname: str


class ShedulernotifyModel(BaseModel, AbsModel):
    queue_name: str = 'sheduler'
    message: str
    queue_after_delay: str
    delay: int