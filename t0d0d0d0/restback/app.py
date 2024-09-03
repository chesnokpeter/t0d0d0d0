from os import umask
from fastapi import FastAPI, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware

from t0d0d0d0.coreback.exceptions import BaseException
from t0d0d0d0.restback.answer import Answer

# from t0d0d0d0.restback.routes.user import userRouter
# from t0d0d0d0.restback.routes.task import taskRouter, inboxRouter
# from t0d0d0d0.restback.routes.project import projectRouter


app = FastAPI(title='t0d0d0d0 api')

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

apiRouter = APIRouter(prefix='/api', tags=['api'])

@apiRouter.get('/ping') 
async def ping():
    return 'pong'

from t0d0d0d0.coreback.services.user import UserService
from t0d0d0d0.restback.depends import uowdep

@apiRouter.get('/a')
async def a(uow = Depends(uowdep)):
    u = await UserService(uow).getOne(6)
    print(u)

# apiRouter.include_router(userRouter)
# apiRouter.include_router(taskRouter)
# apiRouter.include_router(projectRouter)
# apiRouter.include_router(inboxRouter)

@app.exception_handler(BaseException)
async def exception_handler(res, exc: BaseException):  
    return Answer.ErrAnswer(message=exc.errType, desc=exc.message, statuscode=exc.statuscode).make_resp()

app.include_router(apiRouter)