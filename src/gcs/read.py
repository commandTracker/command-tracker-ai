import os

from config.gcs import get_bucket

def get_video(file_name, save_dir):
    bucket = get_bucket()
    blob = bucket.blob(f"edited/{file_name}.mp4")

    blob.download_to_filename(os.path.join(save_dir, f"{file_name}.mp4"))
