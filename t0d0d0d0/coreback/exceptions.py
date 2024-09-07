# class BaseException(Exception):
#     errType = 'Base Error'
#     statuscode = 400

#     def __init__(self, message: str = 'Base Backend Error') -> None:
#         self.message = message


# class AuthException(BaseException):
#     statuscode = 401
#     errType = 'Auth Error'


# class AuthCodeException(AuthException):
#     errType = 'Auth Code Error'


# class JWTException(BaseException):
#     statuscode = 401
#     errType = 'JWT Error'


# class ProjectException(BaseException):
#     errType = 'Project Error'


# class TaskException(BaseException):
#     errType = 'Task Error'


class CoreException(Exception):
    error = 'Base Core Error'

    def __init__(self, desc: str, *args: object) -> None:
        super().__init__(*args)
        self.desc = desc


class UOWException(CoreException): ...


class NoConnectorForRepo(UOWException): ...


class NoAccessForRepo(UOWException): ...


class UserException(CoreException):
    error = 'User Error'


class TaskException(CoreException):
    error = 'Task Error'


class ProjectException(CoreException):
    error = 'Project Error'
