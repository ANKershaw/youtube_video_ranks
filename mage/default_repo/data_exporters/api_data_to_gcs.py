from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from pandas import DataFrame
import pandas as pd
import os
from os import path
from typing import Dict


if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_google_cloud_storage(data_dict: Dict, **kwargs) -> None:
    """
    Template for exporting data to a Google Cloud Storage bucket.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#googlecloudstorage
    """
    # data_dict: {'country':JP, 'country_data':dataFrame}
    country = data_dict['country']

    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    bucket_name = os.environ['GCS_BUCKET_NAME']
    object_key = f'rankings_{country}.parquet'


    GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).export(
        pd.DataFrame(data_dict['country_data']),
        bucket_name,
        object_key,
    )

    print(f'finished saving data for {country}')
   
