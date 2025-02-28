from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    ContentType,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message,
)
from aiogram.utils.deep_linking import decode_payload

from dishka.integrations.aiogram import FromDishka, inject

from ..shortcuts import SUOW, UseCase
from ...app.application.uses_cases.user import BaseUserUseCase
from ...app.domain.repos import AbsUserRepo, AbsEncryptionRepo, AbsMemoryRepo

router = Router()


@router.message(CommandStart())
@inject
async def command_start_handler(message: Message, state: FSMContext, s: SUOW, uc: UseCase[BaseUserUseCase], repo1: FromDishka[AbsUserRepo], repo2: FromDishka[AbsEncryptionRepo], repo3: FromDishka[AbsMemoryRepo]) -> None:
    await state.clear()

    args = message.text.split()
    ref = None
    if len(args) > 1:
        ref = args[1] 

        async with s.uow_repos(uc, repo1, repo2, repo3) as uow:
            code = await uow.uc.service.update_authcode(ref, message.chat.id, message.chat.username)

        await message.answer(
            f'🪪Your code for authorization at <b>t0d0d0d0.com</b>:\n\n<code>{code}</code>\n\nThe code is valid for 30 seconds',
            parse_mode=ParseMode.HTML,
        )
