from litestar import Litestar, Router, Response

import json

from dishka.integrations.litestar import setup_dishka, LitestarProvider
from dishka import make_async_container

from ..app.application.uses_cases.base import UseCaseErrRet

from .jwt.exceptions import JWTError

from .serializer import RestServiceReturn

from .ioc import ioc
from .shortcuts import after_request

from .handlers.user import router as user
from .handlers.project import router as project
from .handlers.task import router as task, inbox

def use_case_err(request, exception: UseCaseErrRet):
    return exception.ret.response

def jwt_err(request, exception: JWTError):
    r = RestServiceReturn(message=exception.type, desc=exception.message, type='error').response
    r.status_code = 401
    return r



def create_app() -> Litestar:

    app = Litestar(
        route_handlers=[Router('/api', route_handlers=[
            inbox,
            user,
            project,
            task
        ])], 
        debug=True, 
        after_request=after_request, 
        exception_handlers={
            UseCaseErrRet:use_case_err,
            JWTError:jwt_err
        }
    )
    container = make_async_container(ioc, LitestarProvider())
    setup_dishka(container, app)
    return app

