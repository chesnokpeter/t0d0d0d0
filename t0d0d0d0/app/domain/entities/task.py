from dataclasses import dataclass, field
from datetime import date as datetype, time as timetype, datetime

from ..shared.enum import TaskStatus


@dataclass(eq=False, slots=True)
class AddTask:
    name: bytes
    createdat: datetime = field(default_factory=datetime.now, kw_only=True)
    date: datetype | None = None
    time: timetype | None = None
    status: TaskStatus = TaskStatus.backlog
    user_id: int
    project_id: int | None = None