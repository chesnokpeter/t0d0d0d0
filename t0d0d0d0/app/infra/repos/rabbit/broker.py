import json

from faststream.rabbit import RabbitBroker

from ....domain.repos import AbsBrokerRepo
from ....domain.interfaces import AbsBrokerMessage


class RabbitmqDefaultRepo(AbsBrokerRepo[RabbitBroker]):
    depends_on = 'RabbitConnector'
    async def send(self, data: AbsBrokerMessage) -> None:
        await self.session.publish(
            json.dumps(data.dict()), data.queue_name
        )
