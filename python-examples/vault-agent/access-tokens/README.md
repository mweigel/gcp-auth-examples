# Vault Agent Example
Vault agent periodically acquires a new token from Vault and writes it to a file. The Python client reads the token and uses it to authenticate to GCP before uploading a file to a bucket. The expiration time of the token is written along with the token itself so the client libraries can determine when it needs to be refreshed.

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

python example.py --project my-gcp-project --bucket my-gcp-bucket --source my-local-file --destination my-uploaded-file --token /path/to/token-data.json
```