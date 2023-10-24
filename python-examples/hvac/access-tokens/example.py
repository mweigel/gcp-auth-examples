import argparse
import hvac
import os

from datetime import datetime
from google.oauth2.credentials import Credentials
from google.cloud import storage


def configure_refresh_handler(client, role, mount_point):
    def refresh_handler(request, *args, **kwargs):
        response = client.secrets.gcp.generate_static_account_oauth2_access_token(
            name=role, mount_point=mount_point
        )

        token = response["data"]["token"]
        expiration_time = datetime.utcfromtimestamp(
            response["data"]["expires_at_seconds"]
        )

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

    client = hvac.Client(
        url=args["url"], namespace=args["namespace"], verify=args["cacert"]
    )
    client.auth.approle.login(
        role_id=os.environ.get("APPROLE_ROLE_ID"),
        secret_id=os.environ.get("APPROLE_SECRET_ID"),
    )

    refresh_handler = configure_refresh_handler(
        client, args["role"], args["mountpoint"]
    )
    credentials = Credentials(token=None, refresh_handler=refresh_handler)

    upload_blob(
        credentials=credentials,
        project=args["project"],
        bucket=args["bucket"],
        source=args["source"],
        destination=args["destination"],
    )
