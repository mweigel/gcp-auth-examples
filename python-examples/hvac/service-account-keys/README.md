# Service Account Key Example

Vault agent acquires a new service account key from Vault and writes it to a file. The Python client reads the service account key and uses it to authenticate to GCP before uploading a file to a bucket. Vault agent takes care of renewing the service account key lease, so as long as Vault agent is running the service account key will not change. Once Vault agent exits, the service account key will be removed from GCP once its lease expires.

# Prerequisites

1. A Google Cloud Platform account with appropriate service accounts configured
1. A Hashicorp Vault server with a [GCP Secrets Engine](https://developer.hashicorp.com/vault/docs/secrets/gcp) configured

## Vault Agent

1. Download and install [Hashicorp Vault](https://developer.hashicorp.com/vault/docs/agent-and-proxy/agent)
1. Update vault-agent-config.hcl with the [appropriate configuration](https://developer.hashicorp.com/vault/docs/agent-and-proxy/agent#configuration) to match your Vault server installation
1. Run Vault agent
```bash
vault agent -config=vault-agent-config.hcl
```

## Python Client

1. Install Python dependencies and run the Python client
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python example.py --project my-gcp-project --bucket my-gcp-bucket --source my-local-file --destination my-uploaded-file --key /path/to/service-account.json
```