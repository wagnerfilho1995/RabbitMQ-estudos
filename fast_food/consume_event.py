import pika
from orders import TAG_APP, TAG_TOTEM

# Establish a connection with RabbitMQ server.
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare exchange (Topico)
channel.exchange_declare(exchange='orders', exchange_type='direct')

# Declare queues (Filas)
channel.queue_declare(queue='app_queue', exclusive=True)
channel.queue_declare(queue='totem_queue', exclusive=True)

# Binding (roteamento)
channel.queue_bind(exchange='orders', queue='app_queue', routing_key="orders.digital.brokenorder.app.api")
channel.queue_bind(exchange='orders', queue='totem_queue', routing_key="orders.digital.brokenorder.totem.api")

# Consume queue
def callback(ch, method, properties, body):
    print(f" [x] Received from {method.routing_key}, body: {body}")
    print(' [*] Waiting for messages. To exit press CTRL+C')


channel.basic_consume(queue='app_queue', on_message_callback=callback, auto_ack=True)
channel.basic_consume(queue='totem_queue', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()