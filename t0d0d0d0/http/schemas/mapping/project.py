from msgspec import defstruct
from typing import NewType

from ....app.domain.schemas import NewProjectSch

NewProjectSch = defstruct('NewProjectSch', NewProjectSch.__annotations__)
NewProjectSch = NewType('NewProjectSch', NewProjectSch)
