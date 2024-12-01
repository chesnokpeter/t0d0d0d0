from dataclasses import dataclass

@dataclass(eq=False, slots=True)
class UserModel:
    id: int
    tgid: bytes
    tgusername: bytes
    name: bytes

    aes_private_key: bytes
    public_key: bytes
    notify_id: int