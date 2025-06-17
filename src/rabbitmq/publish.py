import json
from os import environ

from config.rabbitmq import create_connection

def publish_message(message):
    connection, channel = create_connection()

    channel.basic_publish(
        exchange="",
        routing_key=environ["MQ_PUBLISH_QUEUE"],
        body=json.dumps(message)
    )

    connection.close()
