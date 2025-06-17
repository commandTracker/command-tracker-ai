import datetime
from os.path import join

from config.constants import GCS, MESSAGES
from config.gcs import get_bucket

def generate_signed_url(file_name):
    try:
        bucket = get_bucket()
        blob_name = join(f"results/{file_name}")
        blob = bucket.blob(blob_name)

        url = blob.generate_signed_url(
            version = "v4",
            expiration = datetime.timedelta(minutes=GCS.SIGNED_URL_EXPIRE),
            method = "GET",
        )

        return url
    except:
        raise RuntimeError(MESSAGES.ERROR.FAILED_GENERATE_URL)
