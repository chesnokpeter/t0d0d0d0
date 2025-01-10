
class JWTError(Exception):
    type = 'JWT Error'
    message = 'Error with decoding token'


class ExpiredJWTError(JWTError):
    type = 'JWT Error'
    message = 'Token was expired!'

class InvalidJWTError(JWTError):
    type = 'JWT Error'
    message = 'Invalid token!'

class NotFoundJWTError(JWTError):
    type = 'JWT Error'
    message = 'Token not found in cookie!'
