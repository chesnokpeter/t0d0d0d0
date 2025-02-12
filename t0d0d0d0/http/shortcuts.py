from dishka.integrations.litestar import inject, FromDishka

from typing import Annotated, TypeVar, TypeAlias

from ..app.presentation import ServiceReturn

from litestar import Router, Response
from litestar.handlers.base import BaseRouteHandler
from litestar.routes.base import BaseRoute
from litestar.routes.http import HTTPRoute

from .ioc import RestServiceReturn, SetupUOW, faccess_secure, accST, rshST, frefresh_secure, FREF, FACC

def _process_route_recursively(route: list[BaseRoute]):
    if isinstance(route, HTTPRoute):
        [_process_route_recursively(r) for r in route.route_handlers]
    elif isinstance(route, BaseRouteHandler):
        try:
            route._fn = inject(route._fn)
        except NameError: ...

class DishkaRouter(Router):
    def register(self, value):
        r = super().register(value)
        [_process_route_recursively(r) for r in r]
        return r

async def after_request(response: Response) -> Response:
    if isinstance(response.content, RestServiceReturn):
        return response.content.response
    return response


T = TypeVar('T')

UseCase: TypeAlias = Annotated[FromDishka[T], T]

SUOW: TypeAlias = Annotated[FromDishka[SetupUOW], SetupUOW]

FACCESS: TypeAlias = Annotated[FromDishka[FACC], faccess_secure]

FREFRESH: TypeAlias = Annotated[FromDishka[FREF], frefresh_secure]

accST: TypeAlias = Annotated[FromDishka[accST], accST]
rshST: TypeAlias = Annotated[FromDishka[rshST], rshST]

RET: TypeAlias = ServiceReturn