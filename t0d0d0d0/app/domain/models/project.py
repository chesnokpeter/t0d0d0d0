from dataclasses import dataclass
from datetime import datetime

from .base import BaseModel


@dataclass(eq=False, slots=True)
class ProjectModel(BaseModel):
    id: int
    name: bytes
    createdat: datetime
    user_id: int
