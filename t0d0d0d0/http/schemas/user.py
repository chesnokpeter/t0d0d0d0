from msgspec import Struct

class SignInSch(Struct):
    authcode: str

class CheckAuthcodeSch(Struct):
    authcode: str

