import argparse

from google.oauth2 import service_account
from google.cloud import storage


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
    ap.add_argument("-k", "--key", required=True, help="Service account key file name")

    args = vars(ap.parse_args())

    upload_blob(
        credentials=service_account.Credentials.from_service_account_file(args["key"]),
        project=args["project"],
        bucket=args["bucket"],
        source=args["source"],
        destination=args["destination"],
    )
