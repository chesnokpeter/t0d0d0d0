from dataclasses import dataclass
from ...domain.services import UserService
from ...domain.schemas import SignUpSch
from ...domain.models import UserModel
from .base import BaseUseCase
from .exceptions import service_exceptions

from ...presentation import ServiceReturn



@dataclass(eq=False, slots=True)
class SignUpUseCase(BaseUseCase):
    user_service: UserService

    async def execute(self, data: SignUpSch) -> tuple[ServiceReturn, int | None]:
        try:
            res, private_key_pem, id = await self.user_service.signup(data)
        except service_exceptions as e:
            return ServiceReturn.ErrAnswer(e.type, e.message), None
        except Exception as e:
            raise e

        return ServiceReturn.OkAnswer('sign up', 'successfully created user', [{"private_key":private_key_pem}]), id



@dataclass(eq=False, slots=True)
class SignInUseCase(BaseUseCase):
    user_service: UserService

    async def execute(self, authcode: str) -> tuple[ServiceReturn, int | None]:
        try:
            res, private_key_pem, id = await self.user_service.login(authcode)
        except service_exceptions as e:
            return ServiceReturn.ErrAnswer(e.type, e.message), None
        except Exception as e:
            raise e

        return ServiceReturn.OkAnswer('sign in', 'successfully login user', [{"private_key":private_key_pem}]), id


