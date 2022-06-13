import pika, time, json
from orders import DUMMY_ORDERS, TAG_APP, TAG_TOTEM
from datetime import datetime

# Establish a connection with RabbitMQ server.
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Declare exchange (Topico)
channel.exchange_declare(exchange='orders', exchange_type='direct')

def notify_order(exchange, routing_key, order):
    channel.basic_publish(exchange=exchange, routing_key=routing_key, body=order)
    print(f" [x] Sent to {routing_key}")
    print(f" [x] Body: {order}")


for index, order in enumerate(DUMMY_ORDERS):
    order['generated_at'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    if index % 2 == 0:
        # Let's say it was generated in the app
        notify_order("orders", "orders.digital.brokenorder.app.api", json.dumps(order))
    else:
        # Let's say it was generated in the totem
        notify_order("orders", "orders.digital.brokenorder.totem.api", json.dumps(order))
    time.sleep(5)


connection.close()