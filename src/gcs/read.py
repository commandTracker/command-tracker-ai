from config.constants import MESSAGES
from config.gcs import get_bucket

def get_video(blob_name):
    try:
        bucket = get_bucket()
        blob = bucket.blob(blob_name)

        return blob.open("rb")
    except:
        raise FileNotFoundError(MESSAGES.ERROR.NOT_FOUND_VIDEO)
