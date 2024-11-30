

class ServiceError(Exception):
    def __init__(self, message: str, *args):
        super().__init__(*args)
        self.message = message

class NotFoundError(ServiceError):...

class ConflictError(ServiceError):...

class IncorrectError(ServiceError):...

class PermissionError(ServiceError):...
