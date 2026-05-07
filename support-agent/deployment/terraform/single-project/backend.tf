terraform {
  backend "gcs" {
    bucket = "adk-bigquery-terraform-state"
    prefix = "agent_cli_example/dev"
  }
}
