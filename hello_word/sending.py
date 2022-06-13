import pika

# Establish a connection with RabbitMQ server.
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

msg = "El psy congroo"

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=msg)
                      
print(f" [x] Sent {msg}")

connection.close()