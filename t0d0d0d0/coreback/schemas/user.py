from pydantic import BaseModel

from t0d0d0d0.coreback.models.user import UserModel


class SignUpSch(BaseModel):
    name: str
    authcode: str


class UserSch(UserModel): ...


class NewUserSch(BaseModel):
    tgid: int
    tgusername: str
    name: str
