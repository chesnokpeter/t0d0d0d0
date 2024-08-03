


class BaseExtention(Exception):
    errType = 'Base Error'
    statuscode = 400
    def __init__(self, message: str = 'Base Backend Error') -> None:
        self.message = message

class AuthException(BaseExtention):
    statuscode = 401
    errType = 'Auth Error'

class AuthCodeException(AuthException):
    errType = 'Auth Code Error'

class JWTException(BaseExtention):
    statuscode = 401
    errType = 'JWT Error'

class ProjectException(BaseExtention):
    errType = 'Project Error'