from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from datetime import date as datetype
from datetime import time as timetype
from t0d0d0d0.core.infra.db.enums import TaskStatus



class NewUserModel(BaseModel):
    tgid: int
    tgusername: str
    name: str

class UserModel(NewUserModel):
    id: int


class CleanUserModel(NewUserModel):...



class NewTaskModel(BaseModel):
    name: str
    createdat: datetime = datetime.now()
    date: Optional[datetype] = None
    time: Optional[timetype] = None
    status: TaskStatus = TaskStatus.backlog
    user_id: int
    project_id: Optional['int'] = None

class TaskModel(NewTaskModel):
    id: int

class CleanTaskModel(NewTaskModel):...

class CleanGetTasksModel(NewTaskModel):
    project_name: Optional[str]


class NewProjectModel(BaseModel):
    name: str
    createdat: datetime = datetime.now()
    user_id: int

class ProjectModel(NewProjectModel):
    id: int
class CleanProjectModel(NewProjectModel):...