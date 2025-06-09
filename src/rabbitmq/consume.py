import json
import os
import tempfile

from analyze_video import analyze_video
from config.constants import MESSAGES
from config.rabbitmq import get_channel
from gcs.generate_signed_url import generate_signed_url
from gcs.read import get_video
from gcs.write import upload_video
from rabbitmq.publish import publish_message

def callback(ch, method, properties, body):
    email, file_name, selected_character = json.loads(body).values()

    with tempfile.TemporaryDirectory(dir="temp") as temp_dir:
        try:
            get_video(file_name=file_name, save_dir=temp_dir)
            analyze_video(file_name=file_name, save_dir=temp_dir)

            save_path = os.path.join(temp_dir, "result")

            upload_video(file_name=file_name, save_path=save_path)

            signed_url = generate_signed_url(file_name=file_name)
            message = {
                "email": email,
                "message": MESSAGES.SUCCESS.ANALYZE,
                "url": signed_url
            }
        except Exception as err:
            message = {
                "email": email,
                "message": str(err),
                "url": ""
            }
        publish_message(message=message)

        ch.basic_ack(delivery_tag=method.delivery_tag)

def consume_message():
    channel = get_channel()

    channel.basic_consume(
        queue=os.environ["MQ_CONSUME_QUEUE"],
        auto_ack=False,
        on_message_callback=callback
    )
    channel.start_consuming()
