import os

from config.gcs import get_bucket

def get_video(file_name):
    bucket = get_bucket()
    blob = bucket.blob(f"edited/{file_name}.mp4")
    dir_path = os.path.join(os.path.dirname(os.getcwd()), "temp_video")

    os.makedirs(dir_path, exist_ok=True)

    blob.download_to_filename(os.path.join(dir_path, f"{file_name}.mp4"))

    return
