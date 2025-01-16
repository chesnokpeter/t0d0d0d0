from abc import ABC, abstractmethod
from typing import Any

class AbsMemoryMessage(ABC):
    memory_model_name: str

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.memory_model_name = cls.__name__

    @abstractmethod
    def model_dump(self) -> dict[str, Any]: raise NotImplementedError

