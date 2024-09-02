from pydantic import BaseModel
from datetime import datetime

class ProjectModel(BaseModel):
    id: int
    name: str
    createdat: datetime
    user_id: int