from t0d0d0d0.coreback.models.abstract import MemoryAbsModel
from pydantic import BaseModel

class AuthcodeModel(BaseModel, MemoryAbsModel):
    tgid: int
    tgusername: str

