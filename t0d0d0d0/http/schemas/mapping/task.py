
from msgspec import defstruct
from typing import NewType

from ....app.domain.schemas import NewTaskSch

NewTaskSch = defstruct('NewTaskSch', NewTaskSch.__annotations__)
NewTaskSch = NewType('NewTaskSch', NewTaskSch)