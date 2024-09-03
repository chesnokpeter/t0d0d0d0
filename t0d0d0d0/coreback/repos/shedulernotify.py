from t0d0d0d0.coreback.repos.defaults.rabbitmq import RabbitmqDefaultRepo
from t0d0d0d0.coreback.models.shedulernotify import ShedulernotifyModel

class ShedulernotifyRepo(RabbitmqDefaultRepo[ShedulernotifyModel]):
    model = ShedulernotifyModel
    reponame = 'shedulernotify'