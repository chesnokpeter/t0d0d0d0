from typing import List, Any, Type, TypeVar, Generic, Optional, Literal
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from dataclasses import dataclass, field

T = TypeVar('T')

@dataclass
class Answer:
    message: str
    desc: str
    data: List[dict]
    statuscode: int
    type: Literal['success', 'error']

    def __post_init__(self):
        self._response = self.make_resp()

    def make_resp(self) -> JSONResponse:
        r = {'type': self.type, 'message': self.message, 'desc': self.desc, 'data': [{}]}
        if self.data:
            r['data'] = self.data
        return JSONResponse(r, self.statuscode)
    
    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, value):
        self._response = value


    @staticmethod
    def OkAnswer(message: str, desc: str, data: List[dict[str, Any]]):
        return Answer(type='success', message=message, desc=desc, data=data, statuscode=200)
    
    @staticmethod
    def OkAnswerModel(message: str, desc: str, data: List[BaseModel]|BaseModel):
        if not isinstance(data, list):
            data = [data]
        data = [jsonable_encoder(i) for i in data]
        return Answer.OkAnswer(message=message, desc=desc, data=data)

    @staticmethod
    def ErrAnswer(message: str, desc: str, statuscode:int):
        return Answer(type='error', message=message, desc=desc, data=[{}], statuscode=statuscode)

class AnswerResModel(BaseModel, Generic[T]):
    type: Literal['success', 'error']
    message: str
    desc: str
    data: List[T]