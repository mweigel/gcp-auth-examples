import json
from time import sleep
import google.oauth2.credentials

from datetime import datetime
from googleapiclient.discovery import build

token_path = ""


def refresh_token(request, *args, **kwargs):
    with open(token_path, "r") as token_file:
        token_data = json.load(token_file)

    token = token_data["token"]
    expiration_time = datetime.fromtimestamp(token_data["expires_at_seconds"])

    return token, expiration_time


if __name__ == "__main__":
    credentials = google.oauth2.credentials.Credentials(
        token=None, refresh_handler=refresh_token
    )

    service = build("iam", "v1", credentials=credentials)

    while True:
        result = (
            service.projects()
            .serviceAccounts()
            .keys()
            .list(
                name=f"projects/-/serviceAccounts/service-account-1@project-1.iam.gserviceaccount.com"
            )
            .execute()
        )

        print(result)
        sleep(5)
