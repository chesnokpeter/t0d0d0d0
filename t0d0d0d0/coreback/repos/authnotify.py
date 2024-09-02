from t0d0d0d0.coreback.repos.defaults.rabbitmq import RabbitBroker
from t0d0d0d0.coreback.models.authnotify import AuthnotifyModel

class AuthnotifyRepo(RabbitBroker[AuthnotifyModel]):
    model = AuthnotifyModel