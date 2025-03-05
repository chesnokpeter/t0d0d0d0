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
    CallbackQuery
)
from aiogram.utils.deep_linking import decode_payload

from dishka.integrations.aiogram import FromDishka, inject

from ..shortcuts import SUOW, UseCase
from ...app.application.uses_cases.user import BaseUserUseCase
from ...app.application.uses_cases import NewTaskUseCase, GetByTGIDUseCase, AllInboxUseCase
from ...app.domain.repos import AbsUserRepo, AbsEncryptionRepo, AbsMemoryRepo

from ...app.domain import NewTaskSch

from .utils import send_main_menu, TaskState

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
            f'<b>🎉 You have successfully logged in</b>',
            parse_mode=ParseMode.HTML,
        )
    await send_main_menu(message.answer)



@router.callback_query(lambda callback: callback.data == 'plus_inbox')
async def plus_inbox_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(TaskState.add_inbox)

    await callback.message.answer(
        f'<b>📝 Enter new inbox</b>',
        parse_mode=ParseMode.HTML,
    )


@router.message(TaskState.add_inbox)
@inject
async def plus_inbox_message(message: Message, state: FSMContext, s: SUOW, uc: UseCase[NewTaskUseCase], uc2: UseCase[GetByTGIDUseCase]) -> None:
    await state.clear()

    async with s.uow(uc) as uow:
        async with s.uow(uc2) as uoww:
            r, modell = await uoww.uc.execute(message.chat.id)
        r, model = await uow.uc.execute(modell.id, NewTaskSch(message.text))
        await uow.commit()

    await send_main_menu(message.answer)


@router.callback_query(lambda callback: callback.data == 'list_inbox')
@inject
async def plus_inbox_callback(callback: CallbackQuery, state: FSMContext, s: SUOW, uc: UseCase[AllInboxUseCase], uc2: UseCase[GetByTGIDUseCase]) -> None:
    async with s.uow(uc) as uow:
        async with s.uow(uc2) as uoww:
            r, modell = await uoww.uc.execute(callback.message.chat.id)
        r, model = await uow.uc.execute(modell.id)

    if model:
        await callback.message.answer('\n'.join([i.name for i in model]))

    await send_main_menu(callback.message.answer)
