from pydantic import BaseModel



class SignUpSch(BaseModel):
    name: str
    authcode: str