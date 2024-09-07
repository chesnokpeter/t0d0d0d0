from enum import Enum


class TaskStatus(Enum):
    backlog = 'backlog'
    done = 'done'
    stop = 'stop'
