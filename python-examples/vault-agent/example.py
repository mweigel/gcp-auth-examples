import argparse
import json

from datetime import datetime
from google.oauth2.credentials import Credentials
from google.cloud import storage


def configure_refresh_handler(token_path):
    def refresh_handler(request, *args, **kwargs):
        with open(token_path, "r") as token_file:
            token_data = json.load(token_file)

        token = token_data["token"]
        expiration_time = datetime.fromtimestamp(token_data["expires_at_seconds"])

        return token, expiration_time

    return refresh_handler


def upload_blob(credentials, project, bucket, source, destination):
    storage_client = storage.Client(project=project, credentials=credentials)
    bucket = storage_client.bucket(bucket)
    blob = bucket.blob(destination)

    blob.upload_from_filename(source)

    print(f"File {source} uploaded to {destination}.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--project", required=True, help="GCP project")
    ap.add_argument("-b", "--bucket", required=True, help="Destination bucket")
    ap.add_argument("-s", "--source", required=True, help="Source file name")
    ap.add_argument("-d", "--destination", required=True, help="Destination file name")
    ap.add_argument("-t", "--token", required=True, help="Token file name")

    args = vars(ap.parse_args())

    upload_blob(
        credentials=Credentials(
            token=None,
            refresh_handler=configure_refresh_handler(token_path=args["token"]),
        ),
        project=args["project"],
        bucket=args["bucket"],
        source=args["source"],
        destination=args["destination"],
    )
