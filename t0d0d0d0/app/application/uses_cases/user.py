from dataclasses import dataclass
from ...domain.services import UserService
from ...domain.schemas import SignUpSch
from .base import BaseUseCase

from ...presentation import ServiceReturn

@dataclass(eq=False, slots=True)
class BaseUserUseCase(BaseUseCase):
    service: UserService



@dataclass(eq=False, slots=True)
class SignUpUseCase(BaseUserUseCase):
    async def execute(self, data: SignUpSch) -> tuple[ServiceReturn, int | None]:
        res, private_key_pem, id = await self.call_with_service_excepts(lambda: self.service.signup(data))

        return ServiceReturn.OkAnswer('sign up', 'successfully created user', [{"private_key":private_key_pem}]), id



@dataclass(eq=False, slots=True)
class SignInUseCase(BaseUserUseCase):
    async def execute(self, authcode: str) -> tuple[ServiceReturn, int | None]:
        res, private_key_pem, id = await self.call_with_service_excepts(lambda: self.service.login(authcode))

        return ServiceReturn.OkAnswer('sign in', 'successfully login user', [{"private_key":private_key_pem}]), id

