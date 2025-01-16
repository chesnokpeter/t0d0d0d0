from dataclasses import dataclass, field
from ..interfaces import AbsMemoryMessage

@dataclass(eq=False, slots=True)
class AuthcodeMemory(AbsMemoryMessage):
    tgid: int
    tgusername: str

    def model_dump(self):
        r =  {field: getattr(self, field) for field in self.__annotations__}
        return r
