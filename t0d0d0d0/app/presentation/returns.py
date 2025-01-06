from dataclasses import dataclass
from typing import Any, Generic, Literal, TypeVar

from ..domain.models import BaseModel


@dataclass(eq=False, slots=True)
class ServiceReturn:
    message: str
    desc: str
    data: list[BaseModel]
    type: Literal['success', 'error'] = 'success'
    encrypted: list[str] | None = None


@dataclass(eq=False, slots=True)
class SReturnBuilder:
    returner: ServiceReturn

    def ret(self, message: str, desc: str, data: list[BaseModel], type: Literal['success', 'error'] = 'success', encrypted: list[str] | None = None) ->  ServiceReturn:
        return self.returner(
            message=message,
            desc=desc,
            data=data,
            type=type,
            encrypted=encrypted,
        )

