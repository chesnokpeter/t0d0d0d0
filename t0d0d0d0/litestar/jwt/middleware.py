from dataclasses import dataclass

from litestar import Request

from .secure import Litestar_jwt_secure
from .exceptions import NotFoundJWTError
from ..config import secret_key

accessjwt = Litestar_jwt_secure(secret=secret_key, expire_sec=900)
refreshjwt = Litestar_jwt_secure(secret=secret_key, expire_sec=604800)

@dataclass(eq=False, slots=True)
class User_jwt:
    id: int

async def jwt_secure(request: Request) -> User_jwt:
    if not request.cookies.get('access_token'):
        raise NotFoundJWTError()
    return User_jwt(accessjwt.decode(request.cookies.get('access_token')))

