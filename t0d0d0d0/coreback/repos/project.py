from t0d0d0d0.coreback.infra.postgresql.tables import PROJECT
from t0d0d0d0.coreback.repos.defaults.postgres import PostgresDefaultRepo


class ProjectRepo(PostgresDefaultRepo[PROJECT]):
    model = PROJECT
    reponame = 'project'
