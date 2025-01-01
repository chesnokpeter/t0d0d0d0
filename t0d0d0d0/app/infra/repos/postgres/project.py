from .base import PostgresDefaultRepo
from ...utils.postgres import PROJECT
from ....domain.repos import AbsProjectRepo
from ....domain.models import ProjectModel

class ProjectRepoPostgresql(PostgresDefaultRepo[ProjectModel], AbsProjectRepo):
    table = PROJECT




