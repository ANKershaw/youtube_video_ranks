# Youtube Trending Video Analysis

## Data Source 

The data is from the "Trending YouTube Video Statistics" dataset on Kaggle:

https://www.kaggle.com/datasets/datasnaek/youtube-new

The data is being hosted in GitHub because the JP video file had encoding errors that needed to be corrected. 


## Project Breakdown


## Prerequisites
1. python 3 
1. docker
2. terraform


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
    With Roles:
        Cloud Storage -> Storage Admin
        BigQuery -> BigQuery Admin
        Compute Engine -> Compute Admin 


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

The script will create two files:
mage/.env
terraform/.tfvars

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

From 'youtube_video_ranks/mage' run:
```commandline
# need to mount key location 
docker run -it -p 6789:6789 -v $(pwd):/home/src --env-file ../.env mageai/mageai
```

### Data download / transform / upload with Mage

In your browser, go to :
[localhost:6789](http://localhost:6789/pipelines/youtube_video_ranks/edit?sideview=tree)




### Cleanup

From terraform directory:
```commandline
terraform destroy
```