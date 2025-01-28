from dataclasses import dataclass
from litestar import Request
from typing import TypeAlias

from .secure import Litestar_jwt_secure
from .exceptions import NotFoundJWTError, InvalidJWTError
from ..config import secret_key

accessSecure = Litestar_jwt_secure(secret=secret_key, expire_sec=900, token='access')
refreshSecure = Litestar_jwt_secure(secret=secret_key, expire_sec=604800, token='refresh')

accST: TypeAlias = Litestar_jwt_secure
rshST: TypeAlias = Litestar_jwt_secure

@dataclass(eq=False, slots=True)
class User_jwt:
    id: int

async def jwt_secure(request: Request, accessSecure: accST) -> User_jwt:
    if not request.cookies.get('access_token'):
        raise NotFoundJWTError()
    token = accessSecure.decode(request.cookies.get('access_token'))
    if not token.get('extras') or not token.get('extras').get('token') == 'access':
        raise InvalidJWTError()
    return User_jwt(token)
