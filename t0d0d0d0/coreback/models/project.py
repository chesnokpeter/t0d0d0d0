from datetime import datetime

from pydantic import BaseModel


class ProjectModel(BaseModel):
    id: int
    name: str
    createdat: datetime
    user_id: int
