import jwt

class Litestar_jwt_secure:
    def __init__(self, secret: str):
        self.secret = secret

    def encode(self, id: int) -> str:
        return jwt.encode({"id": str(id)}, self.secret, algorithm="HS256")

    def decode(self, payload: str) -> dict:
        return jwt.decode(payload, self.secret, algorithms="HS256")