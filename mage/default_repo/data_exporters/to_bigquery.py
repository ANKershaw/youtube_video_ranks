from mage_ai.settings.repo import get_repo_path
from mage_ai.io.bigquery import BigQuery
from mage_ai.io.config import ConfigFileLoader
from pandas import DataFrame
import pandas as pd
from os import path
from typing import Dict
import pandas_gbq
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

def create_query(country):
    return f"""
CREATE OR REPLACE TABLE country_data.partitioned_{country} (
  video_id STRING,
  trending_date TIMESTAMP,
  title STRING,
  channel_title STRING,
  category_id STRING,
  publish_time TIMESTAMP,
  tags STRING,
  views STRING,
  likes STRING,
  dislikes STRING,
  comment_count INT64,
  thumbnail_link STRING,
  comments_disabled BOOL,
  ratings_disabled BOOL,
  video_error_or_removed BOOL,
  description STRING,
  country STRING
)
    PARTITION BY DATE(trending_date)
    """

def get_schema():
    return [ {"name": "video_id", "type": "STRING"},
  {"name": "trending_date", "type": "TIMESTAMP"},
  {"name": "title", "type": "STRING"},
  {"name": "channel_title", "type": "STRING"},
  {"name": "category_id", "type": "STRING"},
  {"name": "publish_time", "type": "TIMESTAMP"},
  {"name": "tags", "type": "STRING"},
  {"name": "views", "type": "STRING"},
  {"name": "likes", "type": "STRING"},
  {"name": "dislikes", "type": "STRING"},
  {"name": "comment_count", "type": "INT64"},
  {"name": "thumbnail_link", "type": "STRING"},
  {"name": "comments_disabled", "type": "BOOL"},
  {"name": "ratings_disabled", "type": "BOOL"},
  {"name": "video_error_or_removed", "type": "BOOL"},
  {"name": "description", "type": "STRING"},
  {"name": "country", "type": "STRING"} ]

@data_exporter
def export_data_to_big_query(data_dict: Dict, **kwargs) -> None:
    country = data_dict['country']

    project =  os.environ['GCS_PROJECT_NAME']
    dataset = "country_data"
    table_id = f'{dataset}.partitioned_{country}'

    config_profile = 'default'
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    
    BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).execute(create_query(country))

    data = pd.DataFrame(data_dict['country_data'])
    data['trending_date'] = pd.to_datetime(data['trending_date'])
    data['publish_time'] = pd.to_datetime(data['publish_time'])

    pandas_gbq.to_gbq(data, table_id, project_id=project, table_schema=get_schema())
