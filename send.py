import json

import pika

# Подключение к RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Объявление очереди (без указания durable=True)
channel.queue_declare(queue='in')

# Сообщение, которое вы хотите отправить
message = {'user': 'John Doe', 'user_id': 123}

# Преобразование сообщения в JSON-формат
message_body = json.dumps(message)

# Отправка сообщения в очередь
channel.basic_publish(exchange='', routing_key='in', body=message_body)

print(" [x] Sent 'User registered'")

# Закрытие соединения
connection.close()
