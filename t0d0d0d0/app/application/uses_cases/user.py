from dataclasses import dataclass, field
from ...domain.services import UserService
from ...domain.schemas import SignUpSch
from .base import BaseUseCase

from ...presentation import ServiceReturn, ServiceRetModel

from ...domain.repos import AbsUserRepo, AbsMemoryRepo, AbsBrokerRepo, AbsEncryptionRepo, BaseRepo, AbsProjectRepo, AbsTaskRepo

from ...domain.models import UserModel

@dataclass(eq=False)
class BaseUserUseCase(BaseUseCase):
    service: UserService

    async def execute(self): ...




@dataclass(eq=False)
class SignUpUseCase(BaseUserUseCase):
    repo_used: list[BaseRepo] = field(default_factory=lambda: [AbsUserRepo, AbsMemoryRepo, AbsBrokerRepo, AbsEncryptionRepo, AbsProjectRepo, AbsTaskRepo], init=False)

    async def execute(self, data: SignUpSch) -> ServiceRetModel[int | None]:
        res, private_key_pem, id = await self.call_with_service_excepts(lambda: self.service.signup(data))

        return self.sret.ret('sign up', 'successfully created user', [{"private_key":private_key_pem}]), id



@dataclass(eq=False)
class SignInUseCase(BaseUserUseCase):
    repo_used: list[BaseRepo] = field(default_factory=lambda: [AbsUserRepo, AbsMemoryRepo, AbsBrokerRepo, AbsEncryptionRepo], init=False)

    async def execute(self, authcode: str) -> ServiceRetModel[int | None]:
        res, private_key_pem, id = await self.call_with_service_excepts(lambda: self.service.login(authcode))
        return self.sret.ret('sign in', 'successfully login user', [{"private_key":private_key_pem}]), id

@dataclass(eq=False)
class TestUserUseCase(BaseUserUseCase):
    repo_used: list[BaseRepo] = field(default_factory=lambda: [AbsUserRepo], init=False)

    async def execute(self, user_id: int) -> ServiceReturn:
        res = await self.call_with_service_excepts(lambda: self.service.test(user_id))

        return self.sret.ret('test', 'test successfully done', [res])



@dataclass(eq=False)
class PreregUseCase(BaseUserUseCase):
    repo_used: list[BaseRepo] = field(default_factory=lambda: [AbsUserRepo, AbsMemoryRepo], init=False)

    async def execute(self, authcode: str) -> ServiceRetModel[str]:
        res = await self.call_with_service_excepts(lambda: self.service.prereg(authcode))

        return self.sret.ret('prereg', 'successfully prereg user', [{"authcode":res}]), res



@dataclass(eq=False)
class GetByIdUseCase(BaseUserUseCase):
    repo_used: list[BaseRepo] = field(default_factory=lambda: [AbsUserRepo], init=False)

    async def execute(self, id: int) -> ServiceRetModel[UserModel]:
        res = await self.call_with_service_excepts(lambda: self.service.get_by_id(id))

        return self.sret.ret('profile', 'successfully get profile', [res]), res

