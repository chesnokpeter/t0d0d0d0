from typing import Annotated, TypeVar, TypeAlias

from litestar import Litestar, post, Response, MediaType

from dishka.integrations.litestar import setup_dishka, LitestarProvider, FromDishka, inject
from dishka import make_async_container

from ..app.application.uses_cases.user import TestUserUseCase
from ..app.infra.uow import SetupUOW
from .ioc import ioc, RestServiceReturn


async def after_request(response: Response) -> Response:
    if isinstance(response.content, RestServiceReturn):
        return response.content.response
    return response


T = TypeVar('T')

UseCase: TypeAlias = Annotated[FromDishka[T], T]

SUOW: TypeAlias = Annotated[FromDishka[SetupUOW], SetupUOW]


@post('/')
@inject
async def general(user_id: int, s: SUOW, uc: UseCase[TestUserUseCase]) -> str:
    async with s.uow(uc) as uow:
        r = await uow.uc.execute(user_id)
    return r



def create_app() -> Litestar:
    app = Litestar(route_handlers=[general], debug=True, after_request=after_request)
    container = make_async_container(ioc, LitestarProvider())
    setup_dishka(container, app)
    return app

