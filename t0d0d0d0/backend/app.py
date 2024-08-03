from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from t0d0d0d0.core.exceptions import BaseExtention
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

@app.get('/ping') 
async def ping():
    return 'pong'

app.include_router(userRouter)
app.include_router(taskRouter)
app.include_router(projectRouter)

@app.exception_handler(BaseExtention)
async def exception_handler(res, exc: BaseExtention):  
    return Answer.ErrAnswer(message=exc.errType, desc=exc.message, statuscode=exc.statuscode).make_resp()


