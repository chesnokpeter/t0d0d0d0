from aiogram import Bot
from aiogram.enums import ParseMode
from faststream import FastStream
from faststream.rabbit import RabbitBroker, RabbitQueue
from pydantic import BaseModel, ValidationError

from .schemas import AuthnotifyBroker, TasknotifyBroker

from .сonfig import bot_token, rabbit_url

broker = RabbitBroker(rabbit_url)
app = FastStream(broker)
bot = Bot(bot_token)


def pydantic_model_subscriber(queue: RabbitQueue, model: BaseModel):
    def decorator(func):
        @broker.subscriber(queue)
        async def wrapper(message: str):
            try:
                parsed_message = model.model_validate_json(message)
            except ValidationError as e:
                raise e
            await func(parsed_message)

        return wrapper

    return decorator


broker.pydantic_subscriber = pydantic_model_subscriber


@broker.pydantic_subscriber(RabbitQueue('notifyauth'), AuthnotifyBroker)
async def notyfiauth_handler(data: AuthnotifyBroker):
    await bot.send_message(
        data.tgid,
        '🌐Был совершен вход в ваш аккаунт\n\nЕсли это не вы - то напишите в поддержку <b>@t0d0d0d0support</b>',
        parse_mode=ParseMode.HTML,
    )


@broker.pydantic_subscriber(RabbitQueue('notifytask', durable=True), TasknotifyBroker)
async def notifytask_handler(data: TasknotifyBroker):
    await bot.send_message(data.tgid, f'{data.taskname}\n\nexpired task for\n{data.projname}')
