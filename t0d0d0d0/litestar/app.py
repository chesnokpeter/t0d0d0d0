from litestar import Litestar, post, Request


from dishka.integrations.litestar import setup_dishka, LitestarProvider
from dishka import make_async_container

from ..app.application.uses_cases import TestUserUseCase
from .ioc import ioc

from .shortcuts import DishkaRouter, after_request, UseCase, SUOW

from typing import Any
from litestar.di import Provide
async def di(request: Request):
    print(request)


@post('/', dependencies={'di': Provide(di)})
async def generall(user_id: int, s: SUOW, uc: UseCase[TestUserUseCase], di: Any) -> str:
    async with s.uow(uc) as uow:
        r = await uow.uc.execute(user_id)
    return r




r = DishkaRouter('', route_handlers=[generall])



def create_app() -> Litestar:
    app = Litestar(route_handlers=[r], debug=True, after_request=after_request)
    container = make_async_container(ioc, LitestarProvider())
    setup_dishka(container, app)
    return app

