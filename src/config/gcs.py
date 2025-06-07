from google.cloud import storage
from google.oauth2 import service_account
import os

def get_bucket():
    creds_path = os.path.join(
        os.path.dirname(os.getcwd()),
        os.environ["KEY_FILE_NAME"]
    )
    credentials = service_account.Credentials.from_service_account_file(creds_path)
    storage_client = storage.Client(
        project=os.environ["PROJECT_ID"],
        credentials=credentials
    )
    bucket = storage_client.bucket(os.environ["BUCKET_NAME"])

    return bucket
