from dataclasses import dataclass

@dataclass(eq=False, slots=True)
class SignUp:
    name: str
    authcode: int

