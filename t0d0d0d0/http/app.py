from litestar import Litestar
from litestar.di import Provide

from dishka.integrations.litestar import setup_dishka, LitestarProvider
from dishka import make_async_container

from ..app.application.uses_cases.base import UseCaseErrRet

from .ioc import ioc
from .shortcuts import after_request, jwt_secure

from .handlers.user import router as user

def use_case_err(request, exception: UseCaseErrRet):
    return exception.ret.response



def create_app() -> Litestar:
    app = Litestar(
        route_handlers=[
            user
        ], 
        debug=True, 
        after_request=after_request, 
        dependencies={'di': Provide(jwt_secure)},
        exception_handlers={UseCaseErrRet:use_case_err}
    )
    container = make_async_container(ioc, LitestarProvider())
    setup_dishka(container, app)
    return app

