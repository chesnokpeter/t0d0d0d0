from pydantic import BaseModel

from t0d0d0d0.coreback.models.abstract import BrokerAbsModel


class AuthnotifyModel(BaseModel, BrokerAbsModel):
    queue_name: str = 'notifyauth'
    tgid: int
