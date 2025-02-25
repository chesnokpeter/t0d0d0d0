from pydantic import BaseModel


class AuthnotifyBroker(BaseModel):
    tgid: int

class ShedulernotifyBroker(BaseModel):
    message: str
    queue_after_delay: str
    delay: int

class TasknotifyBroker(BaseModel):
    tgid: int
    taskname: str
    projname: str | None


