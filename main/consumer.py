import pika
import json

from main import Product, db

params = pika.URLParameters(
    'amqps://nejtiavg:amQTJHzYHGABWeLUHL_aMxfO-J9QBL6I@puffin.rmq2.cloudamqp.com/nejtiavg')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')


def callback(channel, method, properties, body):
    print('Received message in main: ', body)
    data = json.loads(body)
    print(data)

    if properties.content_type == 'product_created':
        product = Product(
            id=data['id'], title=data['title'], image=data['image'])
        db.session.add(product)
        db.session.commit()
        print(f'Product created - {product}')

    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        product.title = data['title']
        product.image = data['image']
        db.session.commit()
        print(f'Product updated - {product}')

    elif properties.content_type == 'product_deleted':
        product_id = Product.query.get(data)
        db.session.delete(product_id)
        db.session.commit()
        print(f'Product deleted - {product_id}')


channel.basic_consume(
    queue='main', on_message_callback=callback, auto_ack=True)

print('Started consuming..')

channel.start_consuming()

channel.close()
