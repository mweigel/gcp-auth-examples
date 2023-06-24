import hvac
from time import sleep
import google.oauth2.credentials

from datetime import datetime
from googleapiclient.discovery import build


def refresh_token(request, *args, **kwargs):
    pass


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
