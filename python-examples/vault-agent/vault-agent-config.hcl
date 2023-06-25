vault {
  address = ""
}

auto_auth {
  method {
    type = ""
    config = {}
  }
}

# Retrieve a new token from Vault every 50 minutes.
template_config {
  static_secret_render_interval = "50m"
}

# Output the token to a file along with the token's expiration time.
template {
  contents = "{{ with secret \"path/to/gcp-account/token\" }}{{ .Data | toUnescapedJSON }}{{ end }}"
  destination = "/path/to/token-data.json"
}