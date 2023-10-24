import argparse
import json
import base64
import hvac
import os

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
    ap.add_argument("-u", "--url", required=True, help="Vault server URL")
    ap.add_argument("-r", "--role", required=True, help="Vault role")
    ap.add_argument("-c", "--cacert", required=True, help="Path to CA certificate")
    ap.add_argument("-n", "--namespace", required=True, help="Vault namespace")
    ap.add_argument("-m", "--mountpoint", required=True, help="Vault mountpoint")
    ap.add_argument("-p", "--project", required=True, help="GCP project")
    ap.add_argument("-b", "--bucket", required=True, help="Destination bucket")
    ap.add_argument("-s", "--source", required=True, help="Source file name")
    ap.add_argument("-d", "--destination", required=True, help="Destination file name")

    args = vars(ap.parse_args())

    # Create a client and authenticate to Vault using an approle.
    client = hvac.Client(
        url=args["url"], namespace=args["namespace"], verify=args["cacert"]
    )
    client.auth.approle.login(
        role_id=os.environ.get("APPROLE_ROLE_ID"),
        secret_id=os.environ.get("APPROLE_SECRET_ID"),
    )

    # Read a GCP service account key from Vault. The response contains a base64 encoded Google
    # credentials file stored in the data.private_key_data field.
    response = client.secrets.gcp.generate_static_account_service_account_key(
        name=args["role"], mount_point=args["mountpoint"]
    )
    service_account_info = base64.b64decode(
        response["data"]["private_key_data"]
    ).decode()

    credentials = service_account.Credentials.from_service_account_info(
        json.loads(service_account_info)
    )

    upload_blob(
        credentials=credentials,
        project=args["project"],
        bucket=args["bucket"],
        source=args["source"],
        destination=args["destination"],
    )
