# YouTube Trending Video Analysis

## Problem Statement

YouTube tracks statistics for all videos on the platform and using proprietary methodology, determines which videos are trending. 
The list is unique for each country YouTube serves, meaning that users in the US are seeing a different trending list 
than users in India or Japan. Given this information, what differences are there between trending videos in India, Japab, 
and the United States? 

## Dashboard

Dashboard
0 points: No dashboard
2 points: A dashboard with 1 tile
4 points: A dashboard with 2 tiles



## Data Source 

The data is from the "Trending YouTube Video Statistics" dataset on [Kaggle](https://www.kaggle.com/datasets/datasnaek/youtube-new).
There are many countries to choose from, but we will only use data from India, Japan, and the United States.
The data is being hosted in GitHub because the Japanese file had encoding errors that needed to be corrected. 

There are 6 files in the project. Three files for trending video data:
* INvideos.csv.zip
* JPvideos.csv.zip
* USvideos.csv.zip

And three files that serve as a map for the `category_id` field. These are used in the dbt step as seeds:
* IN_category_id.csv
* JP_category_id.csv
* US_category_id.csv


## Project Breakdown

The project is a series of piplines orchestrated by [Mage](https://www.mage.ai/). There are five distinct parts to the project:
* **Setup**: create GCS project, save credentials locally, run setup script to create GCS bucket and BigQuery schema
* **Phase 1**: import data from API, transform for data lake, save to GCS bucket 
* **Phase 2**: import data from GCS, transform for data warehouse, save to BigQuery
* **Phase 3**: transform BigQuery data using dbt, prepare for dashboard
* **Dashboard**: create dashboard in Looker Studio 

![Flow diagram in three phases. All phases are in a Mage orchestrator.](assets/flow_diagram.png "Flow Diagram for Youtube Trending Data Engineering Project")

### Data Lake
I am using Google Cloud Storage for my data lake, and the data is stored in parquet files:
* rankings_IN.parquet
* rankings_JP.parquet
* rankings_US.parquet


### Data Warehouse
I am using BigQuery for my data warehouse. Data is stored in three datasets: 
* partitioned_IN
* partitioned_JP
* partitioned_US

Each table is partitioned by `trending_date`. The data is not clustered since clustering (and partitioning for that matter)
are not effective for data less than 1GB. These datasets are 48MB, 18MB, and 58MB, respectively.

### Data Transformations
Data is transformed with dbt. 

<details>
    <summary>DAG image</summary>

![Directed Acyclic Graph for dbt workflow](assets/dbt_DAG.png)
</details>

### Orchestrator

The Mage orchestrator runs the three phases mentioned above:
* **Phase 1**: import data from API, transform for data lake, save to GCS bucket 
* **Phase 2**: import data from GCS, transform for data warehouse, save to BigQuery
* **Phase 3**: transform BigQuery data using dbt, prepare for dashboard

<details>
    <summary>Mage Pipelines</summary>

![Explanation of the three Mage pipelines](assets/mage_pipelines.png)
</details>

## Prerequisites

The following need to be installed before you can run this project:
1. Python 3 
2. Terraform
3. Docker

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


## Instructions

### All the steps at once
The steps are explained more below but if you just want to hit the ground running, here are all the steps at once.
If you are on Windows, replace 
This assumes you have done all the prerequisite steps. 

## For Mac / Linux
```commandline
git clone https://github.com/ANKershaw/youtube_video_ranks.git
cd youtube_video_ranks.git
pip install -r requirements.txt
python3 environment_setup.py
cd terraform
terraform init
terraform plan
terraform apply
cd ../mage
chmod +x mage_start.sh
./mage_start.sh
python3 mage_pipelines_automatic.py
```

## For Windows
```commandline
git clone https://github.com/ANKershaw/youtube_video_ranks.git
cd youtube_video_ranks.git
pip install -r requirements.txt
python3 environment_setup.py
cd terraform
terraform init
terraform plan
terraform apply
cd ../mage
./mage_start.bat
python3 mage_pipelines_automatic.py
```

### Clone this repo

``` commandline
git clone https://github.com/ANKershaw/youtube_video_ranks.git
```

### Install Python requirements

```commandline
pip install -r requirements.txt
```

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
python3 mage_pipelines_automatic.py
```

If you want a more interactive experience, try:
```commandline
python3 mage_pipelines_interactive.py
```
Follow the prompts to run the pipelines. 

You can check out the running pipelines by visiting the [Pipeline runs](http://localhost:6789/pipeline-runs) page

## Results
After completing all steps above, you will have the following files:
Google Cloud Storage
* rankings_IN.parquet - API data from INvideos.csv.zip created in Mage pipeline Phase 1
* rankings_JP.parquet - API data from JPvideos.csv.zip created in Mage pipeline Phase 1
* rankings_US.parquet - API data from USvideos.csv.zip created in Mage pipeline Phase 1

BigQuery
Schema: country_data
* partitioned_IN - partitioned table created in Mage pipeline Phase 2
* partitioned_JP - partitioned table created in Mage pipeline Phase 2
* partitioned_US - partitioned table created in Mage pipeline Phase 2
* IN_category_id - seed table created by dbt in Mage pipeline Phase 3
* JP_category_id - seed table created by dbt in Mage pipeline Phase 3
* US_category_id - seed table created by dbt in Mage pipeline Phase 3
* stg_partitioned_IN - stage table created by dbt in Mage pipeline Phase 3
* stg_partitioned_JP - stage table created by dbt in Mage pipeline Phase 3
* stg_partitioned_US - stage table created by dbt in Mage pipeline Phase 3
* dim_categories - dimension table for categories created by dbt in Mage pipeline Phase 3
* fact_trending - fact table of video date created by dbt in Mage pipeline Phase 3


### Cleanup

From terraform directory:
```commandline
terraform destroy
```
