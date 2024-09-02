from t0d0d0d0.coreback.repos.defaults.rabbitmq import RabbitBroker
from t0d0d0d0.coreback.models.shedulernotify import ShedulernotifyModel

class ShedulernotifyRepo(RabbitBroker[ShedulernotifyModel]):
    model = ShedulernotifyModel