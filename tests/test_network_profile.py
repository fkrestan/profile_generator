import os

import pandas
import pytest

import network_profile

HERE = os.path.dirname(os.path.realpath(__file__))


@pytest.mark.parametrize('data_file_path', [
    os.path.join(HERE, 'data', 'test_data.csv')
])
def test_data_load(data_file_path):
   data = network_profile.load_data(data_file_path)

   assert type(data) is pandas.DataFrame
   assert 'bytes' in data.columns
   assert 'packets' in data.columns
   assert 'flow_count' in data.columns


@pytest.mark.parametrize('data_file_path', [
    os.path.join(HERE, 'data', 'test_data.csv')
])
def test_make_profile(data_file_path):
    result = network_profile.make_profile(data_file_path)
    assert type(result) is dict
