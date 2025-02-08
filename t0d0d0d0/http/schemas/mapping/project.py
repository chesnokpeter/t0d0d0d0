from msgspec import defstruct, Struct
from typing import NewType

from ....app.domain.schemas import NewProjectSch

NewProjectSch = defstruct('NewProjectSch', NewProjectSch.__annotations__)
NewProjectSch = NewType('NewProjectSch', NewProjectSch)

class EditProjectSch(Struct):
    id: int
    name: str

class DeleteProjectSch(Struct):
    id: int