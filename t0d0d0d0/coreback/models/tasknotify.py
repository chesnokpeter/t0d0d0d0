from t0d0d0d0.coreback.models.abstract import BrokerAbsModel
from pydantic import BaseModel

class TasknotifyModel(BaseModel, BrokerAbsModel):
    queue_name: str = 'notifytask'
    tgid: int
    taskname: str
