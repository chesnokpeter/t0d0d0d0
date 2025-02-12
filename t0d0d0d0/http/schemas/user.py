from msgspec import Struct

class SignInSch(Struct):
    authcode: str
