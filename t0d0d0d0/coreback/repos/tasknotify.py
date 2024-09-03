from t0d0d0d0.coreback.repos.defaults.rabbitmq import RabbitmqDefaultRepo
from t0d0d0d0.coreback.models.tasknotify import TasknotifyModel

class TasknotifyRepo(RabbitmqDefaultRepo[TasknotifyModel]):
    model = TasknotifyModel
    reponame = 'tasknotify'