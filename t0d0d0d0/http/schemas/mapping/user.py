from msgspec import defstruct
from typing import NewType

from ....app.domain.schemas import SignUpSch

SignUpSch = defstruct('SignUpSch', SignUpSch.__annotations__)
SignUpSch = NewType('SignUpSch', SignUpSch)
