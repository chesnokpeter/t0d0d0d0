from pydantic import BaseModel

from t0d0d0d0.coreback.models.project import ProjectModel


class NewProjectSch(BaseModel):
    name: str


class ProjectSch(ProjectModel): ...
