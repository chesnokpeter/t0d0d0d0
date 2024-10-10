from datetime import datetime, date

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
from t0d0d0d0.coreback.services.task import TaskService

from t0d0d0d0.bot.depends import uowdep, task
from t0d0d0d0.bot.depends import user as userdep

router = Router()


@router.message(Command(commands=['task']))
async def command_task_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    uow = uowdep(task, userdep)
    user = await UserService(uow()).getfromTG(message.chat.id)
    tasks = await TaskService(uow()).getByDate(user.id, datetime.now().date())
    taskstr = ''
    for i in tasks:
        tasks+=i.name+'<b>: '+i.status.value+'</b>\n'

    await message.answer(
        f'<b>Today tasks</b> {taskstr}',
        parse_mode=ParseMode.HTML,
    )
