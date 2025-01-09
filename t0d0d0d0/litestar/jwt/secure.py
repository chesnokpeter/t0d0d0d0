import jwt
from datetime import datetime, timedelta

from .exceptions import ExpiredJWTError, InvalidJWTError, JWTError

class Litestar_jwt_secure:
    __slots__ = ('secret', 'expire_sec', 'extra')

    def __init__(self, secret: str, expire_sec: int, **extra):
        self.secret = secret
        self.expire_sec = expire_sec
        self.extra = extra or {}

    def encode(self, id: int) -> str:
        expire = datetime.now() + timedelta(seconds=self.expire_sec)
        payload = {
            "id": str(id),
            'extras': self.extra,
            'exp': expire
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def decode(self, payload: str) -> dict:
        try:
            return jwt.decode(payload, self.secret, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise ExpiredJWTError()
        except jwt.InvalidTokenError:
            raise InvalidJWTError()
        except jwt.PyJWTError:
            raise JWTError()
        except Exception as e:
            raise e