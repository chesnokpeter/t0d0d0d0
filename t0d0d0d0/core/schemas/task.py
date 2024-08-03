from pydantic import BaseModel
from typing import Optional
from datetime import date as datetype
from datetime import time as timetype
from t0d0d0d0.core.infra.db.enums import TaskStatus


class NewTaskSch(BaseModel):
    name: str
    date: Optional[datetype] = None
    time: Optional[timetype] = None
    status: TaskStatus = TaskStatus.backlog
    project_id: Optional[int] = None

