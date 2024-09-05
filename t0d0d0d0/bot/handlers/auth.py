from datetime import datetime

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

from t0d0d0d0.coreback.services.user import UserService

from t0d0d0d0.bot.depends import uowdep, authcode

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    uow = uowdep(authcode)
    code = await UserService(uow()).newAuthcode(
        tgid=message.chat.id, tgusername=message.chat.username
    )
    await message.answer(
        f'🪪Ваш код для авторизации на <b>t0d0d0d0.com</b>:\n\n<code>{code}</code>\n\nКод действителен в течении 30 секунд',
        parse_mode=ParseMode.HTML,
    )
