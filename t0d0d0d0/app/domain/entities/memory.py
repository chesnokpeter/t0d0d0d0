from dataclasses import dataclass
from ..interfaces import AbsMemoryMessage

@dataclass(eq=False, slots=True)
class AuthcodeMemory(AbsMemoryMessage):
    tgid: int
    tgusername: str

    def model_dump(self):
        return {field: getattr(self, field) for field in self.__annotations__}


