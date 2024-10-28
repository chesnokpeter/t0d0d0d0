from pydantic import BaseModel


class UserModel(BaseModel):
    id: int
    tgid: bytes
    tgusername: bytes
    name: bytes

    aes_private_key: bytes
    public_key: bytes