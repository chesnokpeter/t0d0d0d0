from t0d0d0d0.coreback.models.tasknotify import TasknotifyModel
from t0d0d0d0.coreback.repos.defaults.rabbitmq import RabbitmqDefaultRepo


class TasknotifyRepo(RabbitmqDefaultRepo[TasknotifyModel]):
    model = TasknotifyModel
    reponame = 'tasknotify'
