from enum import Enum

class TaskStatus(Enum):
    backlog = 'backlog'
    done = 'done'
    stop = 'stop'


class REPOS_ALIAS(Enum):
    user = 'user_repo'
    project = 'project_repo'
    task = 'task_repo'
    encryption = 'encryption_repo'
    broker = 'broker_repo'
    memory = 'memory_repo'