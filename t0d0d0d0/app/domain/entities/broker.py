from dataclasses import dataclass

from ..interfaces import AbsBrokerMessage

@dataclass(eq=False, slots=True)
class AuthnotifyBroker(AbsBrokerMessage):
    tgid: int
    queue_name = 'notifyauth'

@dataclass(eq=False, slots=True)
class ShedulernotifyBroker(AbsBrokerMessage):
    message: str
    queue_after_delay: str
    delay: int
    queue_name: str = 'sheduler'

@dataclass(eq=False, slots=True)
class TasknotifyBroker(AbsBrokerMessage):
    tgid: int
    taskname: str
    projname: str | None
    queue_name: str = 'notifytask'


