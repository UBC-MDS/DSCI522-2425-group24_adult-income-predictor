# test_generate_bar_chart_and_save.py
# Author: Quanhua Huang
# Date: 2024-12-13

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.generate_bar_chart_and_save import generate_bar_chart_and_save
import pytest
import pandas as pd

# SETUP

test_dir= 'tests/folder_plot'
plot_1 = 'plot_1.png'

test_df = pd.DataFrame{
    'age': ['10', '20', '27', '56', '33', '20', '27'],
    'marital-status': ['Divorced', 'Divorced', 'Separated', 'Widowed', 'Separated', 'Divorced', 'Widowed']
}
# TESTS

def test_plot_exist():
    generate_bar_chart_and_save(test_df, 
    'age', 
    'Age',
    test_dir, 
    plot_1))
    file_path = os.path.join('tests/folder_plot', plot_1)
    assert os.path.exists(file_path), f"Plot was not saved at {file_path}"
    assert os.path.getsize(file_path) > 0, f"The saved plot exist but is empty at {file_path}"
    os.remove(file_path)

