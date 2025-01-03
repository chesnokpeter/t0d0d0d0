from dataclasses import dataclass, field
from datetime import date as datetype, time as timetype, datetime

from ...shared import TaskStatus

from .base import BaseModel

@dataclass(eq=False, slots=True)
class TaskModel(BaseModel):
    id: int
    name: bytes
    user_id: int
    createdate: datetime = field(default_factory=datetime.now, kw_only=True)
    date: datetype | None = None
    time: timetype | None = None
    status: TaskStatus = TaskStatus.backlog
    project_id: int | None = None

@dataclass(eq=False, slots=True)
class TaskModelWithProjName(TaskModel):
    project_name: bytes | None = None

