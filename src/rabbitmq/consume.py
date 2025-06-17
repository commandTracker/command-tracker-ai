import json
import os

from analyze_video import analyze_frame
from config.constants import MESSAGES
from gcs.generate_signed_url import generate_signed_url
from gcs.read import get_video
from gcs.write import upload_video
from rabbitmq.publish import publish_message
from labeling import label_frames
from extract_frames import extract_frames
from get_commands import get_commands
from create_subtitle import make_stack_ass
from insert_subtitle import insert_subtitle_to_video

def process_message(body):
    try:
        email, file_name, selected_character = json.loads(body).values()
        edited_blob_name = f"edited/{file_name}"

        stream = get_video(blob_name=edited_blob_name)
        data_bytes = stream.read()
        stream.close()

        sit_punch_frames = []
        uppercut_frames = []
        hit_down_frames = []

        try:
            for i, frame in enumerate(extract_frames(data_bytes)):
                pose_data = analyze_frame(frame, side=selected_character)

                label_frames(pose_data, i, sit_punch_frames, uppercut_frames, hit_down_frames)

            commands = get_commands(sit_punch_frames, uppercut_frames, hit_down_frames)
        except:
            raise RuntimeError(MESSAGES.ERROR.FAILED_ANALYZE)

        ass_file_name = f"{file_name}.ass"

        make_stack_ass(commands, ass_file_name)

        output_video_stream = insert_subtitle_to_video(data_bytes, ass_file_name)

        os.remove(ass_file_name)
        upload_video(file_name=file_name, stream=output_video_stream)

        signed_url = generate_signed_url(file_name=file_name)
        message = {
            "email": email,
            "message": MESSAGES.SUCCESS.ANALYZE,
            "url": signed_url
        }

        return message

    except Exception as err:
        message = {
            "email": email,
            "message": str(err),
            "url": ""
        }

    return message

def callback(ch, method, properties, body):
    message = process_message(body)
    publish_message(message)

    ch.basic_ack(delivery_tag=method.delivery_tag)

def consume_message(channel):
    channel.basic_consume(
        queue=os.environ["MQ_CONSUME_QUEUE"],
        auto_ack=False,
        on_message_callback=callback
    )
    channel.start_consuming()
