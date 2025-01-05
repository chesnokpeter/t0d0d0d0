from dataclasses import dataclass
from typing import Any, Generic, Literal, TypeVar
import base64

from ..domain.models import BaseModel


@dataclass(eq=False, slots=True)
class ServiceReturn:
    message: str
    desc: str
    data: list[dict[str, Any]]
    type: Literal['success', 'error']
    encrypted: list[str] | None = None

    @staticmethod
    def OkAnswer(message: str, desc: str, data: list[dict[str, Any]], encrypted: list[str]|None = None):
        return ServiceReturn(
            type='success',
            message=message,
            desc=desc,
            data=data,
            encrypted=encrypted
        )

    @staticmethod
    def OkAnswerModel(message: str, desc: str, data: list[BaseModel] | BaseModel, encrypted: list[str] | None = None):
        if not isinstance(data, list):
            data = [data]

        print(data)

        # def by_encode(val: bytes) -> str:
        #     return base64.b64encode(val).decode('utf-8')

        # def process_value(val):
        #     if isinstance(val, bytes):
        #         return by_encode(val)
        #     elif isinstance(val, list):
        #         return [process_value(item) for item in val]
        #     elif isinstance(val, dict):
        #         return {k: process_value(v) for k, v in val.items()}
        #     else:
        #         return val

        # def process_data(data):
        #     ret = []
        #     for o in data:
        #         item = {}
        #         for name, val in o:
        #             item[name] = process_value(val)
        #         ret.append(item)
        #     return ret
        
        # data = [i.dict() for i in process_data(data)]
        return ServiceReturn.OkAnswer(message=message, desc=desc, data=[{"test":"123"}], encrypted=encrypted)

    @staticmethod
    def ErrAnswer(message: str, desc: str):
        return ServiceReturn(
            type='error',
            message=message,
            desc=desc,
            data=[{}],
        )

