from dataclasses import dataclass, field
from datetime import date as datetype, time as timetype, datetime

from ...shared import TaskStatus


@dataclass(eq=False, slots=True)
class AddTask:
    name: bytes
    user_id: int
    createdat: datetime = field(default_factory=datetime.now, kw_only=True)
    date: datetype | None = None
    time: timetype | None = None
    status: TaskStatus = TaskStatus.backlog
    project_id: int | None = None