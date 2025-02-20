from dataclasses import dataclass

from ..interfaces import AbsBrokerMessage

@dataclass(eq=False, slots=True)
class AuthnotifyBroker(AbsBrokerMessage):
    queue_name = 'notifyauth'
    tgid: int

    def dict(self):
        return {field: getattr(self, field) for field in self.__annotations__}
    
dataclass(eq=False, slots=True)
class ShedulernotifyModel(AbsBrokerMessage):
    queue_name: str = 'sheduler'
    message: str
    queue_after_delay: str
    delay: int
