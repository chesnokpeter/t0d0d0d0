from dataclasses import dataclass, field
from datetime import datetime


@dataclass(eq=False, slots=True)
class AddProject:
    name: bytes
    createdat: datetime = field(default_factory=datetime.now, kw_only=True)
    user_id: int
