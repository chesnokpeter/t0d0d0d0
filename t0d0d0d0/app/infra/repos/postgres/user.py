from .base import PostgresDefaultRepo
from ...utils.postgres import USER
from ....domain.repos import AbsUserRepo
from ....domain.models import UserModel

class UserRepoPostgresql(PostgresDefaultRepo[UserModel], AbsUserRepo):
    table = USER




