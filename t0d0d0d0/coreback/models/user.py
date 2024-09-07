from pydantic import BaseModel


class UserModel(BaseModel):
    id: int
    tgid: int
    tgusername: str
    name: str
