from dataclasses import dataclass
from datetime import date as datetype, time as timetype, datetime

from ..shared.enum import TaskStatus


@dataclass(eq=False, slots=True)
class AddTask:
    name: bytes
    createdat: datetime
    date: datetype | None = None
    time: timetype | None = None
    status: TaskStatus
    user_id: int
    project_id: int | None = None