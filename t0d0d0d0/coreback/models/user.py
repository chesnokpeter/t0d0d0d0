from pydantic import BaseModel


class UserModel(BaseModel):
    id: int
    tgid: int
    tgusername: str
    name: str

    aes_private_key: str
    public_key: str