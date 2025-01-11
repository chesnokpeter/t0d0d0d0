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

from dishka.integrations.aiogram import FromDishka

from ..shortcuts import SUOW, UseCase
from ...app.application.uses_cases.user import BaseUserUseCase
from ...app.domain.repos import AbsUserRepo

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext, s: SUOW, uc: UseCase[BaseUserUseCase], repo: FromDishka[AbsUserRepo]) -> None:
    await state.clear()

    async with s.uow_repos(uc, repo) as uow:
        code = await uow.uc.service.prereg(message.chat.id, message.chat.username)

    await message.answer(
        f'🪪Your code for authorization at <b>t0d0d0d0.com</b>:\n\n<code>{code}</code>\n\nThe code is valid for 30 seconds',
        parse_mode=ParseMode.HTML,
    )
