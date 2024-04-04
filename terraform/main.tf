terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.21.0"
    }
  }
}

provider "google" {
  project     = var.project
  region      = var.region
  credentials = var.auth_key
}

resource "google_storage_bucket" "main-project-bucket" {
  name     = var.gcs_bucket
  location = var.location
}

resource "google_bigquery_dataset" "main-project-dataset" {
  dataset_id                  = var.bigquery_dataset
  location                    = var.region
}