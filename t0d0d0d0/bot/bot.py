import asyncio
import logging
import sys
from typing import NoReturn

from aiogram import Bot, Dispatcher

from t0d0d0d0.bot.handlers.auth import router as messageRouter
# from t0d0d0d0.bot.handlers.task import router as taskRouter
from t0d0d0d0.coreback.config import bot_token

dp = Dispatcher()
bot = Bot(bot_token)


dp.include_router(messageRouter)
# dp.include_router(taskRouter)


async def main() -> NoReturn:
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
