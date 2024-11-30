from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class AddProject:
    name: bytes
    createdat: datetime
    user_id: int
