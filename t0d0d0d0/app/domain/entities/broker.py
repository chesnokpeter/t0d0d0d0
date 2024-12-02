from dataclasses import dataclass

from ..interfaces import AbsBrokerMessage

@dataclass(eq=False, slots=True)
class AuthnotifyBroker(AbsBrokerMessage):
    queue_name = 'notifyauth'
    tgid: int

