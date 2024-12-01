from dataclasses import dataclass

@dataclass(eq=False, slots=True)
class SignUpSch:
    name: str
    authcode: int

