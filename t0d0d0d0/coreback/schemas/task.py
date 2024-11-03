from datetime import date as datetype
from datetime import time as timetype
from typing import Generic, TypeVar

from pydantic import BaseModel

from t0d0d0d0.coreback.models.enums import TaskStatus
from t0d0d0d0.coreback.models.task import TaskModel

T = TypeVar('T')


class TaskSch(TaskModel): ...


class NewTaskSch(BaseModel):
    name: str | bytes
    date: datetype | None = None
    time: timetype | None = None
    status: TaskStatus = TaskStatus.backlog
    project_id: int | None = None


class EditTaskSch(BaseModel, Generic[T]):
    id: int
    edit: T


class NameTaskSch(TaskSch):
    project_name: str | None
