from pydantic import BaseModel

from t0d0d0d0.coreback.models.abstract import BrokerAbsModel


class TasknotifyModel(BaseModel, BrokerAbsModel):
    queue_name: str = 'notifytask'
    tgid: int
    taskname: str
