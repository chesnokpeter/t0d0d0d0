from litestar import Litestar, post
from litestar.di import Provide

from dishka.integrations.litestar import setup_dishka, LitestarProvider
from dishka import make_async_container

from ..app.application.uses_cases import TestUserUseCase
from .ioc import ioc

from .shortcuts import DishkaRouter, after_request, UseCase, SUOW, jwt_secure

from typing import Any


@post('/', dependencies={'di': Provide(jwt_secure)})
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

