from dataclasses import dataclass

from ..interfaces import AbsMemoryMessage

@dataclass(eq=False, slots=True)
class AuthcodeMemory(AbsMemoryMessage):
    tgid: int
    tgusername: str


