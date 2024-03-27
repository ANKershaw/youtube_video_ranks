import io
import pandas as pd
import requests
import zipfile

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """

    url = "https://github.com/ANKershaw/youtube_video_ranks/raw/main/data/youtube_trending/USvideos.csv.zip"
    country = "US"

    # pd.StringDtype() and  pd.Int64Dtype() doesn't work with some of the Japaense videos so we're using object
    video_dtypes = { 
                    'video_id': pd.StringDtype(),
                    'trending_date': object,
                    'channel_title': object,
                    'category_id': pd.StringDtype(),
                    'tags': object,
                    'views': object,
                    'likes': object,
                    'dislikes': object,
                    'comment_count': pd.Int64Dtype(),
                    'thumbnail_link': object,
                    'comments_disabled': pd.BooleanDtype(),
                    'ratings_disabled': pd.BooleanDtype(),
                    'video_error_or_removed': pd.BooleanDtype(),
                    'description': object
    }


    # native date parsing 
    # publish_time is in format '2017-11-12T12:20:39.000Z'
    # trending_date will be transformed later as it is in string format '18.17.02'
    parse_dates = ['publish_time']

    data = pd.read_csv(url, sep=',', dtype=video_dtypes, parse_dates=parse_dates)
    data['country'] = country
    print(f'finished processing for {country}')
    print(data.shape)
    return data

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
