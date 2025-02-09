from msgspec import Struct

class EditProjectSch(Struct):
    id: int
    name: str

class DeleteProjectSch(Struct):
    id: int