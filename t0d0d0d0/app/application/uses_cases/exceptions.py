from ...domain.services import ConflictError, IncorrectError, NotFoundError, PermissionError

service_exceptions = (ConflictError, IncorrectError, NotFoundError, PermissionError)