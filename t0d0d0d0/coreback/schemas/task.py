from pydantic import BaseModel
from typing import TypeVar, Generic

from datetime import date as datetype
from datetime import time as timetype

from t0d0d0d0.coreback.infra.db.models import TaskStatus
from t0d0d0d0.coreback.infra.db.models import TaskModel

T = TypeVar('T')

class TaskSch(TaskModel):...

class NewTaskSch(BaseModel):
    name: str
    date: datetype | None = None
    time: timetype | None = None
    status: TaskStatus = TaskStatus.backlog
    project_id: int | None = None

class EditTaskSch(BaseModel, Generic[T]):
    id: int
    edit: T

class NameTaskSch(TaskSch):
    project_name: str | None
