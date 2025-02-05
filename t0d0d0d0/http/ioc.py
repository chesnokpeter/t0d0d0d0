from dishka import Provider, Scope, provide

from ..app.domain import AbsEncryptionRepo, BaseRepo, NonSession, AbsBrokerRepo, AbsEncryptionRepo, AbsMemoryRepo, AbsProjectRepo, AbsTaskRepo, AbsUserRepo, __all_abs_repos__
from ..app.domain import UserService, ProjectService, TaskService

from ..app.application.uses_cases import RepoRealizations, __all__use_cases__

from ..app.presentation import ServiceReturn, SReturnBuilder

from ..app.infra import EncryptionRepoHazmat, __all_realizations_repos__
from ..app.infra.adapters.postgres import PostgresConnector, get_async_conn_postgres
from ..app.infra.adapters.rabbit import RabbitConnector, get_async_conn_rabbit
from ..app.infra.adapters.redis import RedisConnector, get_async_conn_redis
from ..app.infra import SetupUOW, AbsConnector

from .config import postgres_url, rabbit_url, redis_host, redis_port
from .serializer import RestServiceReturn

from .jwt.middleware import faccess_secure, accST, rshST, accessSecure, refreshSecure

class IoC(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.APP)
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
    def list_connectors(self, pgc: PostgresConnector, rbc: RabbitConnector, rdc: RedisConnector) -> list[AbsConnector]:
        return [pgc, rbc, rdc]

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

[ioc.provide(__all_realizations_repos__[k], provides=v) for k, v in enumerate(__all_abs_repos__)]

ioc.provide(EncryptionRepoHazmat, provides=AbsEncryptionRepo, scope=Scope.APP)

[ioc.provide(i) for i in [UserService, ProjectService, TaskService]]

[ioc.provide(i) for i in __all__use_cases__]

ioc.provide(lambda: accessSecure, provides=accST)

ioc.provide(lambda: refreshSecure, provides=rshST)

ioc.provide(faccess_secure, provides=faccess_secure)

ioc.provide(lambda: RestServiceReturn, provides=ServiceReturn, scope=Scope.APP)

ioc.provide(SReturnBuilder, scope=Scope.APP)

ioc.provide(SetupUOW)

