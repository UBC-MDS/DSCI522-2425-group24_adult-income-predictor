import sys
import os
import pytest
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.validate_raw_file import validate_raw_file 

def test_file_not_exist():
    """
    Test if the function raises FileNotFoundError when the file does not exist.
    """
    non_existent_file = "data/raw/non_existent.data"
    with pytest.raises(FileNotFoundError, match="Unable to find raw file"):
        validate_raw_file(non_existent_file)

def test_invalid_extension(tmp_path):
    """
    Test if the function raises ValueError when the file does not have a .data extension.
    """
    invalid_file = tmp_path / "adult.txt"
    invalid_file.touch() 
    with pytest.raises(ValueError, match="is not a DATA file"):
        validate_raw_file(str(invalid_file))

def test_valid_data_file(tmp_path):
    """
    Test if the function passes validation for a valid .data file.
    """
    valid_file = tmp_path / "adult.data"
    valid_file.touch() 
    try:
        validate_raw_file(str(valid_file))
    except Exception as e:
        pytest.fail(f"validate_raw_file raised an exception for a valid file: {e}")

