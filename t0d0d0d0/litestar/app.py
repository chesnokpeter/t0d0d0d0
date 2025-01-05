import logging

from litestar import Litestar, post
from msgspec import Struct

from dishka.integrations.litestar import setup_dishka, LitestarProvider, FromDishka, inject
from dishka import make_async_container

from ..app.application.uses_cases.user import TestUserUseCase

from ..app.infra.uow import SetupUOW

from .ioc import ioc

class SignUpSch(Struct):
    name: str
    authcode: int



@post('/')
@inject
async def general(user_id: int, s: FromDishka[SetupUOW], uc: FromDishka[TestUserUseCase]) -> str:
    uow = s.uow(uc) 
    async with uow:
        d = await uow.use_case.execute(user_id)
        print(d)
    return '123'






def create_app() -> Litestar:
    app = Litestar(route_handlers=[general], debug=True)
    container = make_async_container(ioc, LitestarProvider())
    setup_dishka(container, app)
    return app

