from dataclasses import dataclass, field
from ...domain.services import UserService
from ...domain.schemas import SignUpSch
from .base import BaseUseCase

from ...presentation import ServiceReturn

from ...domain.repos import AbsUserRepo, AbsMemoryRepo, AbsBrokerRepo, AbsEncryptionRepo, BaseRepo

@dataclass(eq=False)
class BaseUserUseCase(BaseUseCase):
    service: UserService



@dataclass(eq=False)
class SignUpUseCase(BaseUserUseCase):
    repo_used: list[BaseRepo] = field(default_factory=lambda: [AbsUserRepo, AbsMemoryRepo, AbsBrokerRepo, AbsEncryptionRepo], init=False)

    async def execute(self, data: SignUpSch) -> tuple[ServiceReturn, int | None]:
        res, private_key_pem, id = await self.call_with_service_excepts(lambda: self.service.signup(data))

        return ServiceReturn.OkAnswer('sign up', 'successfully created user', [{"private_key":private_key_pem}]), id



@dataclass(eq=False)
class SignInUseCase(BaseUserUseCase):
    repo_used: list[BaseRepo] = field(default_factory=lambda: [AbsUserRepo, AbsMemoryRepo, AbsBrokerRepo, AbsEncryptionRepo], init=False)

    async def execute(self, authcode: str) -> tuple[ServiceReturn, int | None]:
        res, private_key_pem, id = await self.call_with_service_excepts(lambda: self.service.login(authcode))

        return ServiceReturn.OkAnswer('sign in', 'successfully login user', [{"private_key":private_key_pem}]), id

@dataclass(eq=False)
class TestUserUseCase(BaseUserUseCase):
    repo_used: list[BaseRepo] = field(default_factory=lambda: [AbsUserRepo], init=False)

    async def execute(self, user_id: int) -> ServiceReturn:
        res = await self.call_with_service_excepts(lambda: self.service.test(user_id))

        return self.sret.ret('test', 'test successfully done', data=[res])

