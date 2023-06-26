vault {
  address = ""
}

auto_auth {
  method {
    type = ""
    config = {}
  }
}

# Output the service account key to a file.
template {
  contents = "{{ with secret \"path/to/gcp-account/key\" }}{{ base64Decode .Data.private_key_data }}{{ end }}"
  destination = "/path/to/service-account.json"
}