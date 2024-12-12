# eda.py
# Author: Michael Suriawan
# Date: 2024-12-4

import click  
import pandas as pd 
import src.generate_bar_chart_and_save as generate_bar_chart_and_save


@click.command()
@click.option('--processed_dir', type=str, help="Path to processed training data (CSV file)", required=True)
@click.option('--results_dir', type=str, help="Path to the directory where the plots will be saved", required=True)
def main(processed_dir, results_dir):
    """
    Perform exploratory data analysis and generate bar plots.

    Args:
        processed_dir (str): Path to the processed training data in CSV format.
        results_dir (str): Path to the directory where the generated plots will be saved.

    Outputs:
        Six bar plots showing the distribution of income for various categorical variables.
    """
    # Load the dataset from the specified directory
    data_adult = pd.read_csv(processed_dir)
    tup_list = [
        ("Marital Status", "marital-status", "eda1.png"),
        ("Relationships", "relationship", "eda2.png"),
        ("Occupations", "occupation", "eda3.png"),
        ("Workclass", "workclass", "eda4.png"),
        ("Race", "race", "eda5.png"),
        ("Sex", "sex", "eda6.png")
    ]
    for y_axis_label, y_axis_name, plot_name in tup_list:
        generate_bar_chart_and_save(data_adult, y_axis_label, y_axis_name, results_dir, plot_name)

    print("EDA successfully performed and plots saved!")

# Entry point of the script
if __name__ == '__main__':
    main()