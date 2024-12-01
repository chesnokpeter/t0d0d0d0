from dataclasses import dataclass


from .base import BaseModel

@dataclass(eq=False, slots=True)
class UserModel(BaseModel):
    id: int
    tgid: bytes
    tgusername: bytes
    name: bytes

    aes_private_key: bytes
    public_key: bytes
    notify_id: int