from litestar import Request

from ..jwt.secure import Litestar_jwt_secure
from ..config import secret_key

accessjwt = Litestar_jwt_secure(secret=secret_key, expire_sec=900)
refreshjwt = Litestar_jwt_secure(secret=secret_key, expire_sec=604800)

async def jwt_secure(request: Request):
    print(request.cookies)

