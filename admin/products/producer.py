import pika
import json

params = pika.URLParameters(
    'amqps://nejtiavg:amQTJHzYHGABWeLUHL_aMxfO-J9QBL6I@puffin.rmq2.cloudamqp.com/nejtiavg')

connection = pika.BlockingConnection(params)

channel = connection.channel()


if channel.is_closed:
    print('Channel already closed.')

def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(
        exchange='',
        routing_key='main',
        body=json.dumps(body),
        properties=properties
    )
