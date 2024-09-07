from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from t0d0d0d0.coreback.exceptions import CoreException
from t0d0d0d0.restback.exceptions import JWTExceptions

from t0d0d0d0.restback.answer import Answer
from t0d0d0d0.restback.routes.project import projectRouter
from t0d0d0d0.restback.routes.task import inboxRouter, taskRouter
from t0d0d0d0.restback.routes.user import userRouter

app = FastAPI(title='t0d0d0d0 api')

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

apiRouter = APIRouter(prefix='/api', tags=['api'])


@apiRouter.get('/ping')
async def ping():
    return 'pong'


apiRouter.include_router(userRouter)
apiRouter.include_router(taskRouter)
apiRouter.include_router(projectRouter)
apiRouter.include_router(inboxRouter)


@app.exception_handler(JWTExceptions)
async def exception_handler(res, exc: JWTExceptions):
    return Answer.ErrAnswer(message='JWT Error', desc=exc.message, statuscode=401).make_resp()


@app.exception_handler(CoreException)
async def exception_handler(res, exc: CoreException):
    return Answer.ErrAnswer(message=exc.desc, desc=exc.error, statuscode=400).make_resp()


app.include_router(apiRouter)
