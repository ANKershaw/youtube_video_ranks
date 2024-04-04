# Youtube Trending Video Analysis

## Data Source 

The data is from the "Trending YouTube Video Statistics" dataset on Kaggle:

https://www.kaggle.com/datasets/datasnaek/youtube-new

The data is being hosted in GitHub because the JP video file had encoding errors that needed to be corrected. 


## Project Breakdown


## Prerequisites
1. Python 3 
1. Docker
2. Terraform


## Instructions

### Clone this repo

``` commandline
git clone https://github.com/ANKershaw/youtube_video_ranks.git
```

### GCS Project Creation

Create a new project called `youtube-video-ranks` via: https://console.cloud.google.com/projectcreate

## GCS Service Account Creation

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

this script will ask for:
1. Google Cloud project name (should be 'youtube-video-ranks')
2. The name of the bucket you want created (must be unique)
3. Geographical region for the bucket 
4. Location of your google service account key (should be `~/keys/service_account_key.json`)

The script will create the following files:
    terraform/terraform.tfvars
    mage/.env
    mage/mage_start.bat
    mage/mage_start.sh


## Terraform GCS bucket creation

### Install terraform 
Instructions are provided [here](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli).

### Make sure your terraform location and region are correct

Double check the terraform/.tfvars file

## Now run the following from the terraform directory (youtube_video_ranks/terraform):
```commandline
cd terraform

terraform init

terraform plan

terraform apply
```
    

## Mage

Mage is where we will download the data files, process, and upload to GCS. 
<p>There is a pre-configured mage start script in the mage_start.sh and mage_start.bin files to help you get mage started

### For Mac/Linux:
From 'youtube_video_ranks/mage' run:
```commandline
chmod +x mage_start.sh
./mage_start.sh
```

### For Windows:
From 'youtube_video_ranks/mage' run:
```commandline
./mage_start.bat
```

After mage starts, you can check out the pipelines via:
[localhost:6789](http://localhost:6789/pipelines/youtube_video_ranks/edit?sideview=tree)

### Data download / transform / upload with Mage






### Cleanup

From terraform directory:
```commandline
terraform destroy
```