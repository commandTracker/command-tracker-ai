import json
from os import environ

from config.rabbitmq import get_channel
from gcs.read import get_video

def callback(ch, method, properties, body):
    email, file_name, selected_character = json.loads(body).values()

    get_video(file_name=file_name)

def consume_message():
    channel = get_channel()

    channel.basic_consume(
        queue=environ["MQ_CONSUME_QUEUE"],
        auto_ack=False,
        on_message_callback=callback
    )
    channel.start_consuming()
