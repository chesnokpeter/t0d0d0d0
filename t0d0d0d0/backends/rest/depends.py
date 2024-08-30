from fastapi import Security
from datetime import timedelta
from t0d0d0d0.backends.rest.jwt import JwtAccessCookie, JwtRefreshCookie
from t0d0d0d0.core.exceptions import JWTException
from t0d0d0d0.core.config import secret_key

access = JwtAccessCookie(secret_key, False, access_expires_delta=timedelta(minutes=15))
refresh = JwtRefreshCookie(secret_key, False, refresh_expires_delta=timedelta(days=7))

def accessSecure(a = Security(access)):
    if not a:
        raise JWTException(message="invalid jwt token")
    return a

def refreshSecure(a = Security(refresh)):
    if not a:
        raise JWTException(message="invalid jwt token")
    return a