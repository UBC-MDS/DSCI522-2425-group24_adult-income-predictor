# Note: This teardown test data code was adapted from: 
# https://github.com/ttimbers/breast-cancer-predictor/blob/3.0.0/tests/conftest.py

import pytest
import shutil


@pytest.fixture(autouse=True, scope='session')
def cleanup_directories_at_end_of_session():
    # This code will run at the end of the pytest session
    yield

    dirs = [
        'tests/test_zip_data1',
        'tests/test_zip_data2',
        'tests/folder_1',
        'tests/folder_plot'
    ]

    # Code to delete directories goes here
    for directory in dirs:
        try:
            shutil.rmtree(directory)
        except FileNotFoundError:
            pass  # Directory doesn't exist, continue