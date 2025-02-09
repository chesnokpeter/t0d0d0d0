from dataclasses import dataclass
from typing import Literal, TypeAlias, TypeVar, Generic

from ..domain.models import BaseModel


@dataclass(eq=False, slots=True)
class ServiceReturn:
    message: str
    desc: str
    data: list[BaseModel] | None = None
    type: Literal['success', 'error'] = 'success'
    encrypted: list[str] | None = None


@dataclass(eq=False, slots=True)
class SReturnBuilder:
    returner: ServiceReturn

    def ret(self, message: str, desc: str, data: list[BaseModel], encrypted: list[str] | None = None, type: Literal['success', 'error'] = 'success') ->  ServiceReturn:
        return self.returner(
            message=message,
            desc=desc,
            data=data,
            type=type,
            encrypted=encrypted,
        )
    

T = TypeVar('T')

ServiceRetModel: TypeAlias = tuple[ServiceReturn, T]
