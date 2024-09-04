from fastapi import Security
from datetime import timedelta
from t0d0d0d0.restback.jwt import JwtAccessCookie, JwtRefreshCookie
from t0d0d0d0.coreback.exceptions import JWTException
from t0d0d0d0.coreback.config import secret_key, postgres_url, redis_host, redis_port, rabbit_url

from t0d0d0d0.coreback.infra.postgresql import PostgresConnector
from t0d0d0d0.coreback.infra.redis import RedisConnector
from t0d0d0d0.coreback.infra.rabbitmq import RabbitConnector
from t0d0d0d0.coreback.repos.user import UserRepo
from t0d0d0d0.coreback.repos.task import TaskRepo
from t0d0d0d0.coreback.repos.project import ProjectRepo
from t0d0d0d0.coreback.repos.authcode import AuthcodeRepo
from t0d0d0d0.coreback.repos.authnotify import AuthnotifyRepo
from t0d0d0d0.coreback.repos.shedulernotify import ShedulernotifyRepo

from t0d0d0d0.coreback.repos.abstract import AbsRepo

from t0d0d0d0.coreback.uow import UnitOfWork

access = JwtAccessCookie(secret_key, False, access_expires_delta=timedelta(minutes=15))
refresh = JwtRefreshCookie(secret_key, False, refresh_expires_delta=timedelta(days=7))

def accessSecure(a = Security(access)):
    if not a:
        raise JWTException(message="invalid jwt token")
    return a

def refreshSecure(a = Security(refresh)):
    if not a:
        raise JWTException(message="invalid jwt token")
    return a


postgres = PostgresConnector(postgres_url)
redis = RedisConnector(redis_host, redis_port)
rabbit = RabbitConnector(rabbit_url)

connectors = [postgres, redis, rabbit]

user = UserRepo()
task = TaskRepo()
project = ProjectRepo()
authcode = AuthcodeRepo()
authnotify = AuthnotifyRepo()
shedulernotify = ShedulernotifyRepo()

def uowdep(*repos: AbsRepo):
    connectors_name = {i.require_connector for i in repos}
    connectors_done = [i for i in connectors if i.connector_name in connectors_name]
    print(connectors_done)
    return lambda: UnitOfWork(repos, connectors_done)