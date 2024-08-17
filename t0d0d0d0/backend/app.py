from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from t0d0d0d0.core.exceptions import BaseException
from t0d0d0d0.backend.answer import Answer

from t0d0d0d0.backend.routes.user import userRouter
from t0d0d0d0.backend.routes.task import taskRouter
from t0d0d0d0.backend.routes.project import projectRouter



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



apiRouter.include_router(userRouter)
apiRouter.include_router(taskRouter)
apiRouter.include_router(projectRouter)

@app.exception_handler(BaseException)
async def exception_handler(res, exc: BaseException):  
    return Answer.ErrAnswer(message=exc.errType, desc=exc.message, statuscode=exc.statuscode).make_resp()


app.include_router(apiRouter)