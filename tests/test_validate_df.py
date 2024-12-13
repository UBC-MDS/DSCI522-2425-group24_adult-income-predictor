import sys
import os
import click
import pytest
import pandas as pd
import pandera as pa
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.validate_df import validate_df

valid_data = pd.DataFrame({
    "age": [0, 120],
    "workclass": ["Private", "Self-emp-not-inc"],
    "fnlwgt": [10,20],
    "education": ["Bachelors", "Some-college"],
    "education-num": [0, 50],
    "marital-status": ["Married-civ-spouse", "Divorced"],
    "occupation": ["Exec-managerial", "Prof-specialty"],
    "relationship": ["Wife", "Husband"],
    "race": ["Asian-Pac-Islander", "Black"],
    "sex": ["Female", "Male"],
    "capital-gain": [15, 20],
    "capital-loss": [15, 20],
    "hours-per-week": [10, 100],
    "native-country": ["Cambodia", "England"],
    "income": [">50K", "<=50K"]
})

## Case 1: Output is a dataframe
def test_is_dataframe():
    assert isinstance(validate_df(valid_data), pd.DataFrame)

# Case 2: Test for Valid Input Data - No removals through validation in edges of validity
def test_validate_df_valid_input():
    assert validate_df(valid_data).equals(valid_data), "The valid input data was modified unexpectedly."

duplicates = pd.DataFrame({
    "age": [0, 120, 120],
    "workclass": ["Private", "Self-emp-not-inc", "Self-emp-not-inc"],
    "fnlwgt": [10,20,20],
    "education": ["Bachelors", "Some-college", "Some-college"],
    "education-num": [0, 50, 50],
    "marital-status": ["Married-civ-spouse", "Divorced", "Divorced"],
    "occupation": ["Exec-managerial", "Prof-specialty", "Prof-specialty"],
    "relationship": ["Wife", "Husband", "Husband"],
    "race": ["Asian-Pac-Islander", "Black", "Black"],
    "sex": ["Female", "Male", "Male"],
    "capital-gain": [15, 20, 20],
    "capital-loss": [15, 20, 20],
    "hours-per-week": [10, 100, 100],
    "native-country": ["Cambodia", "England", "England"],
    "income": [">50K", "<=50K", "<=50K"]
})

# Case 3: Test for Duplicate Rows
def test_validate_remove_dups():
    result = validate_df(duplicates)
    assert len(result)==2, "The duplicate rows were not dropped"

na_rows = pd.DataFrame({
    "age": [0, 120, np.nan],
    "workclass": ["Private", "Self-emp-not-inc", np.nan],
    "fnlwgt": [10,20,np.nan],
    "education": ["Bachelors", "Some-college", np.nan],
    "education-num": [0, 50, np.nan],
    "marital-status": ["Married-civ-spouse", "Divorced", np.nan],
    "occupation": ["Exec-managerial", "Prof-specialty", np.nan],
    "relationship": ["Wife", "Husband", np.nan],
    "race": ["Asian-Pac-Islander", "Black", np.nan],
    "sex": ["Female", "Male", np.nan],
    "capital-gain": [15, 20, np.nan],
    "capital-loss": [15, 20, np.nan],
    "hours-per-week": [10, 100, np.nan],
    "native-country": ["Cambodia", "England", np.nan],
    "income": [">50K", "<=50K", np.nan]
})

# Case 4: Test for Invalid Input Data - Missing Columns
def test_validate_remove_nan():
    result = validate_df(na_rows)
    assert len(result)==2, "The NAN rows were not dropped"

# Case 5: Test for an empty dataframe
def test_empty_dataframe():
    empty_df = pd.DataFrame(columns=valid_data.columns)
    result = validate_df(empty_df)
    assert result.empty   