import pika

params = pika.URLParameters(
    'amqps://nejtiavg:amQTJHzYHGABWeLUHL_aMxfO-J9QBL6I@puffin.rmq2.cloudamqp.com/nejtiavg')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')


def callback(channel, method, properties, body):
    print('Received message in admin: ', body)


channel.basic_consume(
    queue='admin', on_message_callback=callback, auto_ack=True)

print('Started consuming..')

channel.start_consuming()

channel.close()
