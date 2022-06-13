import pika
import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(f" [x] Received {body}")
    seconds_waiting = body.count(b'.')
    time.sleep(seconds_waiting)
    print(f" [x] Done, waited for {seconds_waiting} seconds.")
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("Waiting for new messages. To exit press CTRL+C'")


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

channel.start_consuming()