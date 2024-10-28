from datetime import datetime

from pydantic import BaseModel


class ProjectModel(BaseModel):
    id: int
    name: bytes
    createdat: datetime
    user_id: int
