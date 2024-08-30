from faststream import FastStream
from faststream.rabbit import RabbitBroker
# from faststream.rabbit import RabbitBroker
# from faststream.nats import NatsBroker
# from faststream.redis import RedisBroker

broker = RabbitBroker("amqp://guest:guest@localhost:5672/")
# broker = NatsBroker("nats://localhost:4222/")
# broker = RedisBroker("redis://localhost:6379/")

app = FastStream(broker)

@broker.subscriber("in")
@broker.publisher("out")
async def handle_msg(user: str, user_id: int) -> str:
    print(user)
    return f"User: {user_id} - {user} registered"