from pydantic import BaseModel

from t0d0d0d0.core.infra.db.models import ProjectModel

class NewProjectSch(BaseModel):
    name: str

class ProjectSch(ProjectModel):...