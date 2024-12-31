from dataclasses import dataclass, field
from datetime import date as datetype, time as timetype, datetime

from ..shared import TaskStatus

from .base import BaseModel

@dataclass(eq=False, slots=True)
class TaskModel(BaseModel):
    id: int
    name: bytes
    createdate: datetime = field(default_factory=datetime.now, kw_only=True)
    date: datetype | None = None
    time: timetype | None = None
    status: TaskStatus
    user_id: int
    project_id: int | None = None

@dataclass(eq=False, slots=True)
class TaskModelWithProjName(TaskModel):
    project_name: bytes

