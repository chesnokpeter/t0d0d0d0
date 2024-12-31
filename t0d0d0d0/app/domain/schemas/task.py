from dataclasses import dataclass

from datetime import date as datetype
from datetime import time as timetype

from ..shared import TaskStatus

@dataclass(eq=False, slots=True)
class NewTaskSch:
    name: str
    date: datetype | None = None
    time: timetype | None = None
    status: TaskStatus = TaskStatus.backlog
    project_id: int | None = None

