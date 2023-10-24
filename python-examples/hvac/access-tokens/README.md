# Access Token Example

The Python client reads the token and uses it to authenticate to GCP before uploading a file to a bucket. The expiration time of the token is written along with the token itself so the client libraries can determine when it needs to be refreshed.

# Prerequisites

1. A Google Cloud Platform account with appropriate service accounts configured
1. A Hashicorp Vault server with a [GCP Secrets Engine](https://developer.hashicorp.com/vault/docs/secrets/gcp) configured

## Python Client

1. Install Python dependencies and run the Python client
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python example.py --project my-gcp-project --bucket my-gcp-bucket --source my-local-file --destination my-uploaded-file
```