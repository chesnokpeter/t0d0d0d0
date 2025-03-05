from aiogram.types import (
    ContentType,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message,
)
from aiogram.enums import ParseMode

async def send_main_menu(answer):
    await answer('<b>🏡 Main menu</b>', parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='➕ inbox', callback_data='plus_inbox'), InlineKeyboardButton(text='➕ today task', callback_data='today_task')],
        [InlineKeyboardButton(text='📅 calendar', callback_data='calendar')],
        [InlineKeyboardButton(text='📃 list inbox', callback_data='list_inbox')]
    ]))