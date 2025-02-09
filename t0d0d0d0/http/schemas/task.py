from typing import Generic, TypeVar
from datetime import datetime
from msgspec import Struct

T = TypeVar('T')

class EditTaskSch(Struct, Generic[T]):
    id: int
    edit: T


class DeleteTaskSch(Struct):
    id: int

class GetTasksByDate(Struct):
    date: datetime

class GetTasksById(Struct):
    id: int