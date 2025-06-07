import datetime
from os.path import join

from config.constants import SIGNED_URL_EXPIRE
from config.gcs import get_bucket

def generate_signed_url(file_name):
    bucket = get_bucket()
    blob_name = join(f"results/{file_name}.avi")
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        version = "v4",
        expiration = datetime.timedelta(minutes=SIGNED_URL_EXPIRE),
        method = "GET",
    )

    return url
