import os

from config.constants import MESSAGES
from config.gcs import get_bucket

def get_video(file_name, save_dir):
    try:
        bucket = get_bucket()
        blob_name = f"edited/{file_name}"
        blob = bucket.blob(blob_name)

        blob.download_to_filename(os.path.join(save_dir, f"{file_name}.mp4"))
    except:
        raise FileNotFoundError(MESSAGES.ERROR.NOT_FOUND_VIDEO)
