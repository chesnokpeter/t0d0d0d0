from dataclasses import dataclass
from datetime import datetime


@dataclass(eq=False, slots=True)
class ProjectModel:
    id: int
    name: bytes
    createdat: datetime
    user_id: int
