from dataclasses import dataclass
from litestar import Request
from typing import TypeAlias

from .secure import Litestar_faccess_secure
from .exceptions import NotFoundJWTError, InvalidJWTError
from ..config import secret_key

accessSecure = Litestar_faccess_secure(secret=secret_key, expire_sec=900, token='access')
refreshSecure = Litestar_faccess_secure(secret=secret_key, expire_sec=604800, token='refresh')

accST: TypeAlias = Litestar_faccess_secure
rshST: TypeAlias = Litestar_faccess_secure

@dataclass(eq=False, slots=True)
class User_jwt:
    id: int

async def faccess_secure(request: Request, accessSecure: accST) -> int:
    if not request.cookies.get('access_token'):
        raise NotFoundJWTError()
    token = accessSecure.decode(request.cookies.get('access_token'))
    if not token.get('extras'):
        raise InvalidJWTError()
    return token['id']


async def frefresh_secure(request: Request, accessSecure: accST) -> int:
    if not request.cookies.get('refresh_token'):
        raise NotFoundJWTError()
    token = accessSecure.decode(request.cookies.get('refresh_token'))
    if not token.get('extras'):
        raise InvalidJWTError()
    return token['id']
