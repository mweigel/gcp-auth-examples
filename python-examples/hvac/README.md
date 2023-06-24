HVAC example

- Program acquires a new token directly from Vault using Hvac
- Python client uses the token to authenticate to GCP

The expiration time of the token is rendered along with the token itself so the client libraries know when it needs to be refreshed (as it's cached in the client).