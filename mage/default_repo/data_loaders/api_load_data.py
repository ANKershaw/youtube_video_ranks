import io
import pandas as pd
from pandas import DataFrame
from typing import Dict, List

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs) -> List[List[Dict]]:
    """
    Template for loading data from API
    """

    urls = [
            ("JP", "https://github.com/ANKershaw/youtube_video_ranks/raw/main/data/youtube_trending/JPvideos.csv.zip"),
            ("IN", "https://github.com/ANKershaw/youtube_video_ranks/raw/main/data/youtube_trending/INvideos.csv.zip"),
            ("US", "https://github.com/ANKershaw/youtube_video_ranks/raw/main/data/youtube_trending/USvideos.csv.zip")
          
        ]
    
    # [ {'country':JP, 'country_data':dataFrame}]
    data_list=[]

    for url in urls:


        # pd.StringDtype() and  pd.Int64Dtype() doesn't work with some of the Japanese videos so we're using object
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

        print(f'started processing for {url[0]}')

        # native date parsing 
        # publish_time is in format '2017-11-12T12:20:39.000Z'
        # trending_date will be transformed later as it is in string format '18.17.02'
        parse_dates = ['publish_time']

        data = pd.read_csv(url[1], sep=',', dtype=video_dtypes, parse_dates=parse_dates)
        data['country'] = url[0]

        print(f'original data has rows, columns: {data.shape}')

        # have to dropna here due to https://github.com/mage-ai/mage-ai/issues/4725 
        data = data.dropna()
        print(f'dropped rows with empty data; data has rows, columns: {data.shape}')

        data_list.append(dict(country=url[0], country_data=data))
        print(f'finished processing for {url[0]}')


    return [
        data_list
    ]
        
     


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
