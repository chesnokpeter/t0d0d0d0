class RestExceptions(Exception): ...


class JWTExceptions(RestExceptions):
    def __init__(self, message: str, *args: object) -> None:
        super().__init__(*args)
        self.message = message


class JWTAccessExceptions(JWTExceptions): ...


class JWTRefreshExceptions(JWTExceptions): ...
