from t0d0d0d0.coreback.repos.defaults.rabbitmq import RabbitBroker
from t0d0d0d0.coreback.models.tasknotify import TasknotifyModel

class TasknotifyRepo(RabbitBroker[TasknotifyModel]):
    model = TasknotifyModel