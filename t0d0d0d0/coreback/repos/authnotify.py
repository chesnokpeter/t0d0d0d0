from t0d0d0d0.coreback.models.authnotify import AuthnotifyModel
from t0d0d0d0.coreback.repos.defaults.rabbitmq import RabbitmqDefaultRepo


class AuthnotifyRepo(RabbitmqDefaultRepo[AuthnotifyModel]):
    model = AuthnotifyModel
    reponame = 'authnotify'
