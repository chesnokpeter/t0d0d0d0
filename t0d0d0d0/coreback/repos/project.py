from t0d0d0d0.coreback.repos.defaults.postgres import PostgresDefaultRepo
from t0d0d0d0.coreback.infra.postgres.tables import PROJECT

class ProjectRepo(PostgresDefaultRepo[PROJECT]):
    model = PROJECT