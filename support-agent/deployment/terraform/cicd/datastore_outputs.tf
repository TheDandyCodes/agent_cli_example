
output "vector_search_collection_id" {
  description = "Vector Search collection ID"
  value       = var.vector_search_collection_id
}

output "pipeline_service_account_emails" {
  description = "Pipeline service account emails by environment"
  value       = { for k, v in google_service_account.vertexai_pipeline_app_sa : k => v.email }
}

output "pipeline_gcs_bucket_names" {
  description = "Pipeline GCS bucket names by environment"
  value       = { for k, v in google_storage_bucket.data_ingestion_pipeline_gcs_root : k => v.name }
}

