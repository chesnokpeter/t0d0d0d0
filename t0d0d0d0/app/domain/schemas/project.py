from dataclasses import dataclass

@dataclass(eq=False, slots=True)
class NewProjectSch:
    name: str

