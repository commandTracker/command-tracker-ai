from os import environ
import pika

_channel = None

def connect():
    global _channel

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(environ["MQ_HOST"])
    )
    _channel = connection.channel()

    _channel.queue_declare(queue=environ["MQ_CONSUME_QUEUE"])
    _channel.queue_declare(queue=environ["MQ_PUBLISH_QUEUE"])

def get_channel():
    global _channel

    if _channel is None:
        raise RuntimeError("채널 연결 실패...")

    return _channel
