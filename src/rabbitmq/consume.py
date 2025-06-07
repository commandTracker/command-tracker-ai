import json
from os import environ

from analyze_video import analyze_video
from config.rabbitmq import get_channel
from gcs.generate_signed_url import generate_signed_url
from gcs.read import get_video
from gcs.write import upload_video
from rabbitmq.publish import publish_message

def callback(ch, method, properties, body):
    email, file_name, selected_character = json.loads(body).values()

    get_video(file_name=file_name)
    analyze_video()
    upload_video(file_name=file_name)
    signed_url = generate_signed_url(file_name=file_name)
    message = {
        "email": email,
        "url": signed_url
    }

    publish_message(message=message)

def consume_message():
    channel = get_channel()

    channel.basic_consume(
        queue=environ["MQ_CONSUME_QUEUE"],
        auto_ack=False,
        on_message_callback=callback
    )
    channel.start_consuming()
