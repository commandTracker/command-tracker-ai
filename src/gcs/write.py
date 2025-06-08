import os

from config.gcs import get_bucket

def upload_video(file_name, save_path):
    bucket = get_bucket()
    result_path = os.path.join(
        save_path,
        f"{file_name}.avi"
    )
    blob_name = os.path.join(f"results/{file_name}.avi")
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(result_path)

    return
