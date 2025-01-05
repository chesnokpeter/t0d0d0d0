from typing import TypeVar
from dishka import Provider, Scope, provide

from ..app.domain.repos import AbsBrokerRepo, AbsEncryptionRepo, AbsMemoryRepo, AbsProjectRepo, AbsTaskRepo, AbsUserRepo, NonSession, BaseRepo

from ..app.infra.repos.encryption import EncryptionRepoHazmat
from ..app.infra.repos.postgres.user import UserRepoPostgresql
from ..app.infra.repos.postgres.project import ProjectRepoPostgresql
from ..app.infra.repos.postgres.task import TaskRepoPostgresql
from ..app.infra.repos.rabbit.broker import BrokerRepoRabbit
from ..app.infra.repos.redis.memory import MemoryRepoRedis

from ..app.domain.services import UserService, ProjectService, TaskService

from ..app.infra.adapters.postgres import PostgresConnector, get_async_conn_postgres
from ..app.infra.adapters.rabbit import RabbitConnector, get_async_conn_rabbit
from ..app.infra.adapters.redis import RedisConnector, get_async_conn_redis

from ..app.application.uses_cases import __all__use_cases__, RepoRealizations

from ..app.infra.uow import SetupUOW
from ..app.infra.adapters import AbsConnector

from .config import postgres_url, rabbit_url, redis_host, redis_port

T = TypeVar('T', bound=BaseRepo)

__abs_repos__ = [AbsBrokerRepo, AbsEncryptionRepo, AbsMemoryRepo, AbsProjectRepo, AbsTaskRepo, AbsUserRepo]

__repos__ = [BrokerRepoRabbit, EncryptionRepoHazmat, MemoryRepoRedis, ProjectRepoPostgresql, TaskRepoPostgresql, UserRepoPostgresql]

class IoC(Provider):
    scope = Scope.REQUEST

    @provide()
    def non_s(self) -> NonSession:
        return NonSession()

    @provide()
    def postgres_conn(self) -> PostgresConnector:
        return PostgresConnector(maker=lambda: get_async_conn_postgres(postgres_url))

    @provide()
    def rabbit_conn(self) -> RabbitConnector:
        return RabbitConnector(maker=lambda: get_async_conn_rabbit(rabbit_url))

    @provide()
    def redis_conn(self) -> RedisConnector:
        return RedisConnector(maker=lambda: get_async_conn_redis(redis_host, redis_port))

    @provide()
    def list_connectors(self, pc: PostgresConnector, rbc: RabbitConnector, rdc: RedisConnector) -> list[AbsConnector]:
        return [pc, rbc, rdc]
    
    @provide()
    def repo_realizations(self, broker: AbsBrokerRepo, encryption: AbsEncryptionRepo, memory: AbsMemoryRepo, project: AbsProjectRepo, task: AbsTaskRepo, user: AbsUserRepo) -> RepoRealizations:
        return {
            AbsUserRepo: user,
            AbsProjectRepo: project,
            AbsTaskRepo: task,
            AbsEncryptionRepo: encryption,
            AbsBrokerRepo: broker,
            AbsMemoryRepo: memory
        }

ioc = IoC()

[ioc.provide(source=__repos__[k], provides=v) for k, v in enumerate(__abs_repos__)]

[ioc.provide(i) for i in [UserService, ProjectService, TaskService]]

[ioc.provide(i) for i in __all__use_cases__]



ioc.provide(SetupUOW)
