# test_read_zip.py
# author: Michael Suriawan
# date: 2024-12-12
# note: This code was adapted from:
# https://github.com/ttimbers/breast-cancer-predictor/blob/3.0.0/tests/test_read_zip.py

import os
import sys
import pytest
import responses
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.read_zip import read_zip


# SETUP

# Test 1 data
test_dir_1 = 'tests/test_zip_data1'
test_dir_1_files = ['test1.txt', 'test2.csv']
url_1 = 'https://github.com/UBC-MDS/DSCI522-2425-group24_adult-income-predictor/raw/refs/heads/main/tests/data/files_txt_csv.zip'

if not os.path.exists(test_dir_1):
    os.makedirs(test_dir_1)

# Test 2 mocks
mock_url = 'https://this_is_a_fake_url.com/some/fake/foo.zip'
# mock non-existing URL
@pytest.fixture
def mock_response():
    # Mock a response with a non-200 status code
    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, mock_url, status=404)
        yield

# Test 3 legit, but non-zip url
url_3 = 'https://github.com/UBC-MDS/DSCI522-2425-group24_adult-income-predictor/raw/refs/heads/main/tests/data/non_zip.csv'


# TESTS

# Test 1: Happy path, `read_csv` should be able to download a zip file with test1.txt and test2.csv
def test_read_zip_txt_csv():
    read_zip(url_1, test_dir_1)
    for file in test_dir_1_files:
        file_path = os.path.join(test_dir_1, file)
        assert os.path.isfile(file_path)

# Test 2: Invalid URL should raise a ValueError
def test_invalid_url(mock_response):
    with pytest.raises(ValueError, match='The URL provided does not exist.'):
        read_zip(mock_url, test_dir_1)

# Test 3: Non-zip URL should raise a ValueError
def test_non_zip_url():
    with pytest.raises(ValueError, match='The URL provided does not point to a ZIP file.'):
        read_zip(mock_url, test_dir_1)