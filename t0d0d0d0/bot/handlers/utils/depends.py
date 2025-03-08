from functools import wraps

from aiogram.fsm.context import FSMContext

from aiogram.types import (
    Message,
    CallbackQuery
)

from ...shortcuts import SUOW, UseCase
from ....app.application.uses_cases import GetByTGIDUseCase


def private_key(func):
    @wraps(func)
    async def wrapper(s: SUOW, uc: UseCase[GetByTGIDUseCase], *args, **kwargs):
        data = await state.get_data()
        if not data.get('id'):
            id: int = None
            for arg in args:
                if isinstance(arg, Message):
                    id = arg.chat.id
                    break
                elif isinstance(arg, CallbackQuery):
                    id = arg.message.chat.id
                    break

            async with s.uow(uc) as uow:
                r, model = await uow.uc.execute(id)

                await state.set_data(id=model.id, private_key=uow.uc.service.encryption_repo.aes_decrypt(model.aes_private_key, uow.uc.service.encryption_repo.convert_tgid_to_aes_key(id)))


        r = await func(*args, **kwargs)
        return r
    return wrapper


