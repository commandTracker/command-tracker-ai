import json
from os import environ

from config.rabbitmq import get_channel

def callback(ch, method, properties, body):
    email, file_name, selected_character = json.loads(body).values()

def consume_message():
    channel = get_channel()

    channel.basic_consume(
        queue=environ["MQ_CONSUME_QUEUE"],
        auto_ack=False,
        on_message_callback=callback
    )
    channel.start_consuming()
