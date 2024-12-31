from dataclasses import dataclass

from .uow import AbsUnitOfWork
from .uses_cases import BaseUseCase, UseCaseErrRet
from ..presentation import ServiceReturn

@dataclass(eq=False, slots=True)
class Use:
    use_case: BaseUseCase
    uow: AbsUnitOfWork

    async def __call__(self, *args, **kwds, ) -> ServiceReturn:
        async with self.uow as uow:
            uc = await self.use_case.execute(*args, **kwds)


