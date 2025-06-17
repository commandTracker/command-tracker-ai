from os import environ
import pika
import time

from config.constants import MESSAGES, RABBITMQ

def create_connection(retry=0):
    if retry >= 5:
        raise RuntimeError(MESSAGES.ERROR.FAILED_CONNECT_CHANNEL)

    try:
        params = pika.URLParameters(environ["MQ_HOST"])
        params.heartbeat = RABBITMQ.HEART_BEAT

        connection = pika.BlockingConnection(params)
        channel = connection.channel()

        channel.queue_declare(queue=environ["MQ_CONSUME_QUEUE"], durable=True)
        channel.queue_declare(queue=environ["MQ_PUBLISH_QUEUE"], durable=True)

        return connection, channel
    except:
        time.sleep(5)

        return create_connection(retry + 1)
