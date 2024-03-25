variable "location" {
  description = "the GCS location (country) for your bucket"
  default     = "US"
}

variable "region" {
  description = "the GCS region for your bucket"
  default     = "us-west1"
}

variable "project" {
  description = "the name of the GCS project"
  default     = "youtube-video-ranks"
}

variable "gcs_bucket" {
  description = "where the youtube video ranks files will be stored in GCS"
  default     = "youtube-video-ranks-bucket"
}

variable "auth_key" {
  description = "the location/name of the credential file for the GSC service account."
  default     = "./key/service_account_key.json"
}