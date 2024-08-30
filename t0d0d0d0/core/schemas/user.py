from pydantic import BaseModel

from t0d0d0d0.core.infra.db.models import UserModel

class SignUpSch(BaseModel):
    name: str
    authcode: str

class UserSch(UserModel):...

class NewUserSch(BaseModel):
    tgid: int
    tgusername: str
    name: str 