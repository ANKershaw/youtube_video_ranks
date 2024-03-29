from typing import Dict, List
import pandas as pd



if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data_dict: Dict, *args, **kwargs) -> Dict:
    # data_dict: {'country':JP, 'country_data':dataFrame}
    country = data_dict['country']
    print(f'transforming data for {country}')

    data = pd.DataFrame(data_dict['country_data'])
    data = data.drop_duplicates()

    # trending_date is in string format '18.17.02'
    data['trending_date'] = pd.to_datetime(data['trending_date'], format="%y.%d.%m")
    data_dict['country_data'] = data.dropna().reset_index(drop=True)

    print(f'finished transforming data for {country}. data has rows, columns: {data.shape}') 

    return data_dict




@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
