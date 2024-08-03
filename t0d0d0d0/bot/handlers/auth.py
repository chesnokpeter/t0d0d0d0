from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message, ContentType, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, CommandObject, Command
from aiogram.utils.deep_linking import decode_payload
from datetime import datetime
from fastapi import Depends
from t0d0d0d0.core.services.user import UserService
from t0d0d0d0.core.depends import uowdep, infra, anonuow

router = Router()

@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.clear() 
    uow = anonuow(infra=infra(db=False, memory=True))
    code = await UserService(uow()).newAuthcode(tgid=message.chat.id, tgusername=message.chat.username)
    await message.answer(f"🪪Ваш код для авторизации на <b>t0d0d0d0.com</b>:\n\n<code>{code}</code>\n\nКод действителен в течении 30 секунд", parse_mode=ParseMode.HTML)


