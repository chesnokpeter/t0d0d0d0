from datetime import date as datetype
from datetime import datetime
from datetime import time as timetype

from pydantic import BaseModel, ConfigDict

from t0d0d0d0.coreback.models.enums import TaskStatus


class TaskModel(BaseModel):
    id: int
    name: bytes
    createdat: datetime
    date: datetype | None
    time: timetype | None
    status: TaskStatus
    user_id: int
    project_id: int | None

    model_config = ConfigDict(arbitrary_types_allowed=True)
