from t0d0d0d0.coreback.infra.postgresql.tables import USER
from t0d0d0d0.coreback.repos.defaults.postgres import PostgresDefaultRepo


class UserRepo(PostgresDefaultRepo[USER]):
    model = USER
    reponame = 'user'
