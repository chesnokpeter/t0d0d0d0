from pydantic import BaseModel

from t0d0d0d0.coreback.models.abstract import BrokerAbsModel


class ShedulernotifyModel(BaseModel, BrokerAbsModel):
    queue_name: str = 'sheduler'
    message: str
    queue_after_delay: str
    delay: int
