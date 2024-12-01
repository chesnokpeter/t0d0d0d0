

class ServiceError(Exception):
    type = 'Service Error'
    def __init__(self, message: str, *args):
        super().__init__(*args)
        self.message = message

class NotFoundError(ServiceError):
    type = 'Not Found Error'

class ConflictError(ServiceError):
    type = 'Conflict Error'

class IncorrectError(ServiceError):
    type = 'Incorrect Error'

class PermissionError(ServiceError):
    type = 'Permission Error'
