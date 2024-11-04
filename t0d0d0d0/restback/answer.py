from dataclasses import dataclass
from typing import Any, Generic, Literal, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import base64

T = TypeVar('T')


@dataclass
class Answer:
    message: str
    desc: str
    data: list[dict]
    statuscode: int
    type: Literal['success', 'error']
    encrypted: list[str] | None = None

    def __post_init__(self):
        self._response = self.make_resp()

    def make_resp(self) -> JSONResponse:
        r = {
            'type': self.type,
            'message': self.message,
            'desc': self.desc,
            'data': [{}],
        }
        if self.data:
            r['data'] = self.data
        if self.encrypted:
            r['encrypted'] = self.encrypted
        return JSONResponse(r, self.statuscode)

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, value):
        self._response = value

    @staticmethod
    def OkAnswer(message: str, desc: str, data: list[dict[str, Any]], encrypted: list[str]|None = None):
        return Answer(
            type='success',
            message=message,
            desc=desc,
            data=data,
            statuscode=200,
            encrypted=encrypted
        )

    @staticmethod
    def OkAnswerModel(message: str, desc: str, data: list[BaseModel] | BaseModel, encrypted: list[str]|None = None):
        if not isinstance(data, list):
            data = [data]

        def by_encode(val: bytes):
            return base64.b64encode(val).decode('utf-8')

        def process_value(val):
            if isinstance(val, bytes):
                return by_encode(val)
            elif isinstance(val, list):
                return [process_value(item) for item in val]
            elif isinstance(val, dict):
                return {k: process_value(v) for k, v in val.items()}
            else:
                return val

        def process_data(data):
            ret = []
            for o in data:
                item = {}
                for name, val in o:
                    item[name] = process_value(val)
                ret.append(item)
            return ret
        
        data = [jsonable_encoder(i) for i in process_data(data)]
        return Answer.OkAnswer(message=message, desc=desc, data=data, encrypted=encrypted)

    @staticmethod
    def ErrAnswer(message: str, desc: str, statuscode: int):
        return Answer(
            type='error',
            message=message,
            desc=desc,
            data=[{}],
            statuscode=statuscode,
        )


class AnswerResModel(BaseModel, Generic[T]):
    type: Literal['success', 'error']
    message: str
    desc: str
    data: list[T]
