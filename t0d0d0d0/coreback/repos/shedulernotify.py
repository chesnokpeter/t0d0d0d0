from t0d0d0d0.coreback.models.shedulernotify import ShedulernotifyModel
from t0d0d0d0.coreback.repos.defaults.rabbitmq import RabbitmqDefaultRepo


class ShedulernotifyRepo(RabbitmqDefaultRepo[ShedulernotifyModel]):
    model = ShedulernotifyModel
    reponame = 'shedulernotify'
