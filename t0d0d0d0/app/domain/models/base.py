from dataclasses import dataclass
from typing import Any
from abc import ABC

@dataclass(eq=False, slots=True)
class BaseModel(ABC):
    def dict(self) -> dict[str, Any]:
        return {field: getattr(self, field) for field in self.__annotations__}
