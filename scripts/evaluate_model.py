# evaluate_model.py
# Author: Michael Suriawan
# Date: 2024-12-4
# Description: This script evaluates a machine learning model using test data and generates a confusion matrix plot.

import os
import click
import pickle
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay


@click.command()
@click.option('--x_dir', type=str, help="Path to X_test CSV file", required=True)
@click.option('--y_dir', type=str, help="Path to y_test CSV file", required=True)
@click.option('--pickle_loc', type=str, help="Path to the pickle file containing the trained model", required=True)
@click.option('--results_figure_dir=', type=str, help="Path to the directory where the plots will be saved", required=True)
@click.option('--results_table_dir', type=str, help="Path to the directory where the table will be saved", required=True)
def main(x_dir, y_dir, pickle_loc, results_figure_dir, results_table_dir):
    """
    Main function to evaluate a model's performance on test data.
    
    Parameters:
        x_dir(str): Path to the CSV file containing test features.
        y_dir (str): Path to the CSV file containing test labels.
        results_dir (str): Directory to save evaluation results (e.g., confusion matrix).
        table_dir (str): Directory to save final prediction score.
        pickle_loc (str): Path to the pickle file containing the trained model.
    
    Outputs:
        - Prints the model's test score.
        - Saves the confusion matrix plot to the specified results directory.
    """
    # Load the trained model from the pickle file
    with open(pickle_loc, 'rb') as f:
        model = pickle.load(f)
    
    # Load test datasets
    X_test = pd.read_csv(x_dir)  # Features for testing
    y_test = pd.read_csv(y_dir)  # Labels for testing

    # Calculate the model's test score, and save it to a CSV file
    test_score = model.score(X_test, y_test)
    print(f"The model obtained a final test score of: {test_score}")
    test_score_file = os.path.join(results_table_dir, "test_score.csv")
    pd.DataFrame({'test_score': [test_score]}).to_csv(test_score_file, index=False)

    # Generate and save the confusion matrix plot
    ConfusionMatrixDisplay.from_estimator(
        model,
        X_test,
        y_test,
        values_format="d"  # Format values as integers
    )

    # Save the confusion matrix plot to the results directory
    cm_path = os.path.join(results_figure_dir, "cm.png")
    plt.savefig(cm_path, dpi=300, bbox_inches='tight')
    plt.close()  

    print("Model evaluation completed successfully!")


if __name__ == '__main__':
    main()
