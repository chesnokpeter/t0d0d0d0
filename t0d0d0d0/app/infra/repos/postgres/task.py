from .base import PostgresDefaultRepo
from ...utils.postgres import TASK
from ....domain.repos import AbsTaskRepo
from ....domain.models import TaskModel

class TaskRepoPostgresql(PostgresDefaultRepo[TaskModel], AbsTaskRepo):
    table = TASK

    #! get_all_with_proj_name implement!!


