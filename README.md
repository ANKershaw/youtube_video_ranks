# YouTube Trending Video Analysis

## Data Source 

The data is from the "Trending YouTube Video Statistics" dataset on Kaggle:

https://www.kaggle.com/datasets/datasnaek/youtube-new

The data is being hosted in GitHub because the JP video file had encoding errors that needed to be corrected. 

## Problem Statement

## Project Breakdown

### Diagram

### Problem description
 Problem is well described and it's clear what the problem the project solves

Cloud
2 points: The project is developed in the cloud
4 points: The project is developed in the cloud and IaC tools are used
Data ingestion (choose either batch or stream)
Batch / Workflow orchestration
4 points: End-to-end pipeline: multiple steps in the DAG, uploading data to data lake

Data warehouse
4 points: Tables are partitioned and clustered in a way that makes sense for the upstream queries (with explanation)
Transformations (dbt, spark, etc)
4 points: Tranformations are defined with dbt, Spark or similar technologies
Dashboard
0 points: No dashboard
2 points: A dashboard with 1 tile
4 points: A dashboard with 2 tiles
Reproducibility
0 points: No instructions how to run the code at all
2 points: Some instructions are there, but they are not complete
4 points: Instructions are clear, it's easy to run the code, and the code works


## Prerequisites

The following need to be installed before you can run this project:
1. Python 3 
2. Terraform
3. Docker


## Instructions

### Clone this repo

``` commandline
git clone https://github.com/ANKershaw/youtube_video_ranks.git
```

### Install Python requirements

```commandline
pip install -r requirements.txt
```


### GCS Project Creation

Create a new project called `youtube-video-ranks` via: https://console.cloud.google.com/projectcreate

### GCS Service Account Creation

https://console.cloud.google.com/iam-admin/serviceaccounts
Create a service account in your Google Cloud project 
IAM & Admin -> Service Accounts -> Create a Service Account 
<p>With Roles:

* Cloud Storage -> Storage Admin
* BigQuery -> BigQuery Admin
* Compute Engine -> Compute Admin 


Note: this is meant to be a demo and the permissions granted above are overly broad. 
https://cloud.google.com/docs/authentication/application-default-credentials

Service Account -> Actions -> Manage Keys -> Create a New Key -> JSON
    Save this json file to `~/keys/service_account_key.json`

### Environment file

Create project variable files by running:

```commandline
python3 environment_setup.py
```
This script will ask for:
1. Google Cloud project name (eg: 'youtube-video-ranks')
2. The name of the bucket you want created (must be unique)
3. Geographical region for the bucket (default: US)
4. Region for the bucket (default: us-west1)
5. Location of your Google service account key (should be `~/keys/service_account_key.json`)

The script will create the following files:
    terraform/terraform.tfvars
    mage/.env
    mage/mage_start.bat
    mage/mage_start.sh


### Terraform GCS bucket creation

Run the following from the terraform directory (youtube_video_ranks/terraform):
```commandline
cd terraform

terraform init

terraform plan

terraform apply
```
    

### Mage

Mage is where we will download the data files, process, and upload to GCS. 
<p>There is a pre-configured mage start script in the mage_start.sh and mage_start.bin files to help you get mage started

#### For Mac/Linux:
From 'youtube_video_ranks/mage' run:
```commandline
chmod +x mage_start.sh
./mage_start.sh
```

#### For Windows:
From 'youtube_video_ranks/mage' run:
```commandline
./mage_start.bat
```

After mage starts, you can check out the pipelines via:
[localhost:6789](http://localhost:6789/pipelines/youtube_video_ranks/edit?sideview=tree)

### Data download / transform / upload with Mage

There are 3 mage pipelines, and each one can be independently run in case of error.

Phase 1 : Move data from API to GCS
Phase 2 : Move data from GCS to BigQuery
Phase 3 : Create views with dbt 

The pipelines can be executed by running:
```commandline
python3 mage_pipelines.py
```

Follow the prompts to run the pipelines. 


### Cleanup

From terraform directory:
```commandline
terraform destroy
```
