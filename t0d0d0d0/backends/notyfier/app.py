# consumer_service.py
from faststream import FastStream
from faststream.rabbit import RabbitBroker

broker = RabbitBroker("amqp://guest:guest@localhost:5672/")
app = FastStream(broker)

@broker.subscriber("authnotify")
async def handle_message(message: str):
    print(f"Received message: {message}")

if __name__ == "__main__":
    app.run()