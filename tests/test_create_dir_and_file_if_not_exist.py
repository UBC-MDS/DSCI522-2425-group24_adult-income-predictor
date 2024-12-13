# test_create_dir_and_file_if_not_exist.py
# author: Michael Suriawan
# date: 2024-12-12 

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.create_dir_and_file_if_not_exist import create_dir_and_file_if_not_exist

# SETUP

test_dir_1 = 'tests/folder_1'
file_1 = 'file_1.csv'

# TESTS

# Test 1: Happy path, create_dir_and_file_if_not_exist should perform correctly
def test_create_dir_and_file_if_not_exist():
    expected = test_dir_1 + '/' + file_1
    actual = create_dir_and_file_if_not_exist(test_dir_1, file_1)
    assert expected == actual, f"Expected path {expected}, but got {actual}"