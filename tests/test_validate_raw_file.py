import sys
import os
import tempfile
import pytest
import pandas as pd
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.validate_raw_file import validate_raw_file 

def test_valid_file():
    """Test with a valid .data file."""
    with tempfile.NamedTemporaryFile(suffix=".data", delete=False) as valid_file:
        try:
            validate_raw_file(valid_file.name)
        finally:
            os.unlink(valid_file.name) 

def test_invalid_extension():
    """Test with a file that doesn't have the .data extension."""
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as invalid_file:
        try:
            with pytest.raises(ValueError) as excinfo:
                validate_raw_file(invalid_file.name)
            assert "is not a DATA file" in str(excinfo.value)
        finally:
            os.unlink(invalid_file.name) 

def test_nonexistent_file():
    """Test with a file that doesn't exist."""
    nonexistent_file = "nonexistent.data"
    with pytest.raises(FileNotFoundError) as excinfo:
        validate_raw_file(nonexistent_file)
    assert "Unable to find raw file" in str(excinfo.value)
