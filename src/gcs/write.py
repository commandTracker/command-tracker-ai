import os

from config.gcs import get_bucket

def upload_video(file_name):
    bucket = bucket = get_bucket()
    result_path = os.path.join(
        os.path.dirname(os.getcwd()),
        "detect",
        "result",
        f"{file_name}.avi"
    )
    blob_name = os.path.join(f"results/{file_name}.avi")
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(result_path)

    return
