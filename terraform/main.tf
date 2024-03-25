terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.21.0"
    }
  }
}

provider "google" {
  # or do export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/key"
  credentials = var.auth_key
  project     = var.project
  region      = var.region
}

resource "google_storage_bucket" "main-project-bucket" {
  name     = var.gcs_bucket
  location = var.location

}