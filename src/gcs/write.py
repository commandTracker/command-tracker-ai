import os

from config.constants import MESSAGES
from config.gcs import get_bucket

def upload_video(file_name, stream):
    try:
        bucket = get_bucket()
        blob_name = os.path.join(f"results/{file_name}")
        blob = bucket.blob(blob_name)

        blob.upload_from_file(stream,rewind=True, content_type="video/webm")
    except:
        raise FileNotFoundError(MESSAGES.ERROR.FAILED_UPLOAD)
