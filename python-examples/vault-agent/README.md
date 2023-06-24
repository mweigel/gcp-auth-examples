Vault Agent Example

- Vault agent acquires and renders a new token from Vault periodically
- Python client uses the token to authenticate to GCP

Run Vault agent using:
vault agent -config=./vault-agent-config.hcl

The expiration time of the token is rendered along with the token itself so the client libraries know when it needs to be refreshed (as it's cached in the client).