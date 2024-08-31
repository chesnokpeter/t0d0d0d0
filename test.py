import pika

# Параметры подключения к RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Объявляем очередь (если она не существует, она будет создана)
channel.queue_declare(queue='authnotify', durable=True)

# Сообщение, которое хотим отправить
message = "notyf!!!!!!i"

# Отправка сообщения в очередь
channel.basic_publish(
    exchange='',
    routing_key='authnotify',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=2,  # make message persistent
    ))

print(f" [x] Sent '{message}'")

# Закрываем соединение
connection.close()