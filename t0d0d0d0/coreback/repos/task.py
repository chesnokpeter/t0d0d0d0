from t0d0d0d0.coreback.repos.defaults.postgres import PostgresDefaultRepo
from t0d0d0d0.coreback.infra.postgresql.tables import TASK

class TaskRepo(PostgresDefaultRepo[TASK]):
    model = TASK
    reponame = 'task'