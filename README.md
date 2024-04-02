# Youtube Trending Video Analysis

## Data Source 

The data is from the "Trending YouTube Video Statistics" dataset on Kaggle:

https://www.kaggle.com/datasets/datasnaek/youtube-new

The data is being hosted in github because the JP video file had encoding errors that needed to be corrected. 


## Project Breakdown


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

create the environment file and change the location of the key as needed

```commandline
cp .env.bak .env
```

Note: if your .json key is not located at `~/keys/service_account_key.json`,
Change the key location in the following places:
`youtube_video_ranks/terraform/variables.tf [auth_key][default`
`youtube_video_ranks/.env`

## Terraform GCS bucket creation

### Install terraform 
Instructions are provided [here](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli).

### Make sure your terraform location and region are correct

Change `location` and `region` data as needed in: 
    `youtube_video_ranks/terraform/variables.tf`


## Now run the following from the terraform directory (youtube_video_ranks/terraform):
```commandline
terraform init

terraform plan

terraform apply
```
    

## Mage

Mage is where we will download the data files, process, and upload to GCS. 

From 'youtube_video_ranks/mage' run:
```commandline
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