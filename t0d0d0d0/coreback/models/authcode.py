from pydantic import BaseModel

from t0d0d0d0.coreback.models.abstract import MemoryAbsModel


class AuthcodeModel(BaseModel, MemoryAbsModel):
    tgid: int
    tgusername: str
