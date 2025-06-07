import json
from os import environ

from config.rabbitmq import get_channel

def publish_message(message):
    channel = get_channel()

    channel.basic_publish(
        exchange="",
        routing_key=environ["MQ_PUBLISH_QUEUE"],
        body=json.dumps(message)
    )
