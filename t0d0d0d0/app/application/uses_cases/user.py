from dataclasses import dataclass, field
from ...domain.services import UserService
from ...domain.schemas import SignUpSch
from .base import BaseUseCase

from ...presentation import ServiceReturn, ServiceRetModel

from ...domain.repos import AbsUserRepo, AbsMemoryRepo, AbsBrokerRepo, AbsEncryptionRepo, BaseRepo, AbsProjectRepo, AbsTaskRepo

from ...domain.models import UserModel

from ...domain.entities import AuthcodeMemory

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

@dataclass(eq=False)
class GenNewAuthcodeUseCase(BaseUserUseCase):
    repo_used: list[BaseRepo] = field(default_factory=lambda: [AbsMemoryRepo], init=False)

    async def execute(self) -> ServiceRetModel[str]:
        res = await self.call_with_service_excepts(lambda: self.service.gen_new_authcode())
        return self.sret.ret('new authcode', 'successfully create authcode', [{'authcode':res}]), res

@dataclass(eq=False)
class CheckAuthcodeUseCase(BaseUserUseCase):
    repo_used: list[BaseRepo] = field(default_factory=lambda: [AbsMemoryRepo], init=False)

    async def execute(self, code: str) -> ServiceRetModel[AuthcodeMemory | None]:
        res = await self.call_with_service_excepts(lambda: self.service.check_authcode(code))

        return self.sret.ret('check', 'successfully checked authcode', [res]), res


@dataclass(eq=False)
class AuthcodeSignUpUseCase(BaseUserUseCase):
    repo_used: list[BaseRepo] = field(default_factory=lambda: [AbsUserRepo, AbsMemoryRepo, AbsBrokerRepo, AbsEncryptionRepo, AbsProjectRepo, AbsTaskRepo], init=False)

    async def execute(self, authcode: str) -> ServiceRetModel[int | None]:
        res, private_key_pem, id = await self.call_with_service_excepts(lambda: self.service.signup_authcode(authcode))

        return self.sret.ret('sign up', 'successfully created user', [{"private_key":private_key_pem}]), id



@dataclass(eq=False)
class AuthcodeSignInUseCase(BaseUserUseCase):
    repo_used: list[BaseRepo] = field(default_factory=lambda: [AbsUserRepo, AbsMemoryRepo, AbsBrokerRepo, AbsEncryptionRepo], init=False)

    async def execute(self, authcode: str) -> ServiceRetModel[int | None]:
        res, private_key_pem, id = await self.call_with_service_excepts(lambda: self.service.login_authcode(authcode))
        return self.sret.ret('sign in', 'successfully login user', [{"private_key":private_key_pem}]), id



@dataclass(eq=False)
class GetByTGIDUseCase(BaseUserUseCase):
    repo_used: list[BaseRepo] = field(default_factory=lambda: [AbsUserRepo, AbsEncryptionRepo], init=False)

    async def execute(self, tgid: int) -> ServiceRetModel[UserModel | None]:
        res = await self.call_with_service_excepts(lambda: self.service.get_by_tgid(tgid))

        return self.sret.ret('user', 'successfully get user', [res]), res
