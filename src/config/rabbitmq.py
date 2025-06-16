from os import environ
import pika
import time

from config.constants import MESSAGES

_channel = None

def connect(retry=0):
    global _channel

    if retry >= 5:
        raise RuntimeError(MESSAGES.ERROR.FAILED_CONNECT_CHANNEL)

    try:
        params = pika.URLParameters(environ["MQ_HOST"])
        connection = pika.BlockingConnection(params)
        _channel = connection.channel()

        _channel.queue_declare(queue=environ["MQ_CONSUME_QUEUE"], durable=True)
        _channel.queue_declare(queue=environ["MQ_PUBLISH_QUEUE"], durable=True)
    except:
        time.sleep(5)
        connect(retry + 1)

def get_channel():
    global _channel

    if _channel is None:
        connect(retry=0)

    return _channel
