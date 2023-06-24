vault {
  address = ""
}

auto_auth {
  method {
    type = "token_file"
    config = {
      token_file_path = ""
    }
  }
}

template_config {
  exit_on_retry_failure = true
  static_secret_render_interval = "50m"
}

template {
  contents = "{{ with secret \"gcp/static-account/service-account-1/token\" }}{{ .Data | toUnescapedJSON }}{{ end }}"
  destination = "./token-data.json"
}