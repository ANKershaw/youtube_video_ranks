import pandas as pd
from pandas import DataFrame

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data: DataFrame):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """

    # trending_date is in string format '18.17.02'

    country = "JP"
    print(f'original data shape for {country}: {data.shape}')
    data = data.drop_duplicates().dropna()

    data['trending_date'] = pd.to_datetime(data['trending_date'], format="%y.%d.%m")
    
    print(f'finished processing data for {country}: {data.shape}')

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
