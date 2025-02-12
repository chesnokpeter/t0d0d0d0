from typing import Generic, TypeVar
from datetime import date
from msgspec import Struct

from datetime import date as datetype
from datetime import time as timetype

from ...app.shared import TaskStatus

T = TypeVar('T')

class EditTaskSch(Struct, Generic[T]):
    id: int
    edit: T


class DeleteTaskSch(Struct):
    id: int

class GetTasksByDate(Struct):
    date: date

class GetTasksById(Struct):
    id: int


class NewTaskSch(Struct):
    name: str
    date: datetype | None = None
    time: timetype | None = None
    status: TaskStatus = TaskStatus.backlog
    project_id: int | None = None

