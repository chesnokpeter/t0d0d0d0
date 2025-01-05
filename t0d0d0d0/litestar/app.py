import logging, dishka

import dishka.plotter
from litestar import Litestar, post
from msgspec import Struct

from dishka.integrations.litestar import setup_dishka, LitestarProvider, FromDishka, inject
from dishka import make_async_container

from ..app.application.uses_cases.user import TestUserUseCase

from ..app.infra.uow import SetupUOW, UnitOfWork

from .ioc import ioc

class SignUpSch(Struct):
    name: str
    authcode: int



@post('/')
@inject
async def general(user_id: int, s: FromDishka[SetupUOW], uc: FromDishka[TestUserUseCase]) -> str:
    async with s.uow(uc) as uow:
        uow: UnitOfWork[TestUserUseCase]
        r = await uow.use_case.execute(user_id)
    return r






def create_app() -> Litestar:
    app = Litestar(route_handlers=[general], debug=True)
    container = make_async_container(ioc, LitestarProvider())
    print(dishka.plotter.render_mermaid(container))
    setup_dishka(container, app)
    return app

