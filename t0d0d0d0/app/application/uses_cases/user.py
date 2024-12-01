from dataclasses import dataclass
from ...domain.services import UserService
from ...domain.schemas import SignUpSch
from ...domain.models import UserModel
from .base import BaseUseCase

@dataclass(eq=False, slots=True)
class SignUpUseCase(BaseUseCase):
    user_service: UserService

    async def execute(self, data: SignUpSch) -> tuple[UserModel, bytes]:



        executive = lambda: self.user_service.signup(data)
        await executive()
        return await self.user_service.signup(data)