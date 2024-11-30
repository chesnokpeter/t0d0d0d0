from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class ProjectModel:
    id: int
    name: bytes
    createdat: datetime
    user_id: int
