# eda.py
# Author: Michael Suriawan
# Date: 2024-12-4
# Description: This script performs exploratory data analysis (EDA) on a processed dataset and generates bar plots 
#              showing income distribution based on various categorical variables. The plots are saved to a specified directory.

import click  
import os
import altair as alt  
import pandas as pd 


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

    # Generate bar plot for income by marital status
    eda1 = alt.Chart(data_adult, title="Income for different marital status").mark_bar(opacity=0.75).encode(
        alt.Y('marital-status').title("Marital Status"),
        alt.X('count()').stack(False),
        alt.Color('income')
    ).properties(
        height=200,
        width=300
    )

    # Generate bar plot for income by relationship status
    eda2 = alt.Chart(data_adult, title="Income for different relationship").mark_bar(opacity=0.75).encode(
        alt.Y('relationship').title("Relationships"),
        alt.X('count()').stack(False),
        alt.Color('income')
    ).properties(
        height=200,
        width=300
    )

    # Generate bar plot for income by occupation
    eda3 = alt.Chart(data_adult, title="Income for different occupation").mark_bar(opacity=0.75).encode(
        alt.Y('occupation').title("Occupations"),
        alt.X('count()').stack(False),
        alt.Color('income')
    ).properties(
        height=200,
        width=300
    )

    # Generate bar plot for income by workclass
    eda4 = alt.Chart(data_adult, title="Income for different workclass").mark_bar(opacity=0.75).encode(
        alt.Y('workclass').title("Workclass"),
        alt.X('count()').stack(False),
        alt.Color('income')
    ).properties(
        height=200,
        width=300
    )

    # Generate bar plot for income by race
    eda5 = alt.Chart(data_adult, title="Income for different race").mark_bar(opacity=0.75).encode(
        alt.Y('race').title("Race"),
        alt.X('count()').stack(False),
        alt.Color('income')
    ).properties(
        height=200,
        width=300
    )

    # Generate bar plot for income by sex
    eda6 = alt.Chart(data_adult, title="Income for different sex").mark_bar(opacity=0.75).encode(
        alt.Y('sex').title("Sex"),
        alt.X('count()').stack(False),
        alt.Color('income')
    ).properties(
        height=200,
        width=300
    )

    # Create the output directory if it does not exist
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir, exist_ok=True)

    # Save each plot to the results directory
    eda1.save(os.path.join(results_dir, "eda1.png"), scale_factor=2.0)
    eda2.save(os.path.join(results_dir, "eda2.png"), scale_factor=2.0)
    eda3.save(os.path.join(results_dir, "eda3.png"), scale_factor=2.0)
    eda4.save(os.path.join(results_dir, "eda4.png"), scale_factor=2.0)
    eda5.save(os.path.join(results_dir, "eda5.png"), scale_factor=2.0)
    eda6.save(os.path.join(results_dir, "eda6.png"), scale_factor=2.0)

    print("EDA successfully performed and plots saved!")

# Entry point of the script
if __name__ == '__main__':
    main()
