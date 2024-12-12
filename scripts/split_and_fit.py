# split_and_fit.py
# author: Michael Suriawan
# date: 2024-12-04
# description: This script processes a dataset by performing data validation, preprocessing, 
#              training a K-Nearest Neighbors classifier, and saving the trained model. 
#              It includes data integrity checks using Deepchecks and handles categorical 
#              and binary features appropriately.

import os
import click
import pandas as pd
import pickle
from sklearn.compose import make_column_transformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from deepchecks.tabular import Dataset
from deepchecks.tabular.checks import FeatureLabelCorrelation
from deepchecks.tabular.checks.data_integrity import FeatureFeatureCorrelation
from deepchecks.tabular.checks import ClassImbalance


@click.command()
@click.option('--processed_dir', type=str, help="Path to processed training data (CSV file)", required=True)
@click.option('--preprocessed_dir', type=str, help="Path to save split data", required=True)
@click.option('--random_seed', type=int, help="Random seed that will be used in data split", required=True)
@click.option('--models_dir', type=str, help="Path to the directory where the model will be saved", required=True)
def main(processed_dir, preprocessed_dir, random_seed, models_dir):
    """
    Main function to process data, validate it, train a KNN classifier, and save the trained model.

    Parameters:
    -----------
    processed_dir : str
        Path to the processed training data in CSV format.
    results_dir : str
        Path to the directory where the trained model and any results will be saved.
    random_seed : int
        Selected seed for test data split

    Workflow:
    ---------
    1. Load the dataset from the specified CSV file.
    2. Split the dataset into training and testing sets.
    3. Perform data validation checks:
        a. Check for class imbalance in the target variable.
        b. Check feature-label correlation.
        c. Check feature-feature correlation.
    4. Preprocess the data by handling categorical and binary features.
    5. Train a K-Nearest Neighbors classifier.
    6. Save the trained model as a pickle file.
    """
    
    # Load the dataset from the specified directory
    data_adult = pd.read_csv(processed_dir)
    print(f"Loaded data from {processed_dir} with shape {data_adult.shape}")

    # Data Split: Split the data into training and testing sets (80% train, 20% test)
    train_df, test_df = train_test_split(data_adult, test_size=0.20, random_state=random_seed)
    X_train, y_train = (
        train_df.drop(columns=['income']),
        train_df["income"],
    )
    X_test, y_test = (
        test_df.drop(columns=['income']),
        test_df["income"],
    )

    X_test_file = os.path.join(preprocessed_dir, "X_test.csv")
    X_test.to_csv(X_test_file, index=False)

    y_test_file = os.path.join(preprocessed_dir, "y_test.csv")
    y_test.to_csv(y_test_file, index=False)

    print(f"Split data into train (shape: {X_train.shape}) and test (shape: {X_test.shape}) sets")

    # Validation 3: Target and Response distribution using Deepchecks
    adult_train_ds = Dataset(train_df, label="income", cat_features=[])
    target_counts = train_df["income"].value_counts()
    print(f"Target distribution:\n{target_counts}")

    # Check for class imbalance: Ensure that no class ratio is less than 40%
    check_dist = ClassImbalance().add_condition_class_ratio_less_than(0.4).run(adult_train_ds)
    if not check_dist.passed_conditions():
        raise ValueError("Class imbalance check failed: Target classes do not meet the required distribution.")

    print("Data Validation 3 passed: The target has at least a 40%/60% split!")

    # Validation 4: Deepcheck Validations for Feature-Label and Feature-Feature Correlations
    # Check Feature-Label Correlation: Ensure no feature has a Pearson correlation > 0.9 with the label
    check_feat_label_corr = FeatureLabelCorrelation().add_condition_feature_pps_less_than(0.9)
    check_feat_label_corr_result = check_feat_label_corr.run(dataset=adult_train_ds)
    
    if not check_feat_label_corr_result.passed_conditions():
        raise ValueError("Feature-Label correlation check failed: One or more features exceed the correlation threshold.")

    # Check Feature-Feature Correlation: Ensure no more than 3 feature pairs have correlation > 0.8
    check_feat_feat_corr = FeatureFeatureCorrelation().add_condition_max_number_of_pairs_above_threshold(0.8, 3)
    check_feat_feat_corr_result = check_feat_feat_corr.run(dataset=adult_train_ds)
    
    if not check_feat_feat_corr_result.passed_conditions():
        raise ValueError("Feature-Feature correlation check failed: Too many highly correlated feature pairs.")

    print("Data Validation 4 passed: Deep checks validation has been performed successfully!")

    # Column selection: Define which features are categorical, binary, or to be dropped
    categorical_features = ["marital-status", "relationship", "occupation", "workclass", "race"]
    binary_features = ["sex"]
    drop_features = ["age", "fnlwgt", "education", "education-num", "capital-gain", "capital-loss", "hours-per-week", "native-country"]
    
    print(f"Categorical features: {categorical_features}")
    print(f"Binary features: {binary_features}")
    print(f"Features to drop: {drop_features}")

    # Preprocessing pipelines for different feature types
    # Binary features are one-hot encoded, dropping one category to avoid multicollinearity
    binary_transformer = OneHotEncoder(drop="if_binary", dtype=int)

    # Categorical features are imputed with a constant ('missing') and then one-hot encoded
    categorical_transformer = make_pipeline(
        SimpleImputer(strategy="constant", fill_value="missing"),
        OneHotEncoder(handle_unknown="ignore", sparse_output=False),
    )

    # Combine transformers into a column transformer
    preprocessor = make_column_transformer(   
        (binary_transformer, binary_features),    
        (categorical_transformer, categorical_features),
        ("drop", drop_features),
    )

    print("Preprocessing pipeline created.")

    # Initialize the K-Nearest Neighbors classifier
    model = KNeighborsClassifier()
    print("Initialized KNeighborsClassifier.")

    # Create a pipeline that first preprocesses the data and then fits the model
    pipe = make_pipeline(preprocessor, model)
    print("Pipeline created with preprocessing and KNN model.")

    # Fit the pipeline on the training data
    pipe.fit(X_train, y_train)
    print("Pipeline fitted on the training data.")

    # Evaluate the model's training score
    train_score = pipe.score(X_train, y_train)
    print(f"Training score: {train_score:.4f} obtained")

    # Create the directory if it doesn't exist
    if not os.path.isdir(models_dir):
        os.makedirs(models_dir, exist_ok=True)
        
    # Save the trained pipeline (including preprocessing and model) as a pickle file
    model_path = os.path.join(models_dir, "model.pickle")
    with open(model_path, 'wb') as f:
        pickle.dump(pipe, f)
    print(f"Successfully saved the trained model to {model_path}")

    print("Successfully split data and trained the model. A PICKLE file has been created!")


if __name__ == '__main__':
    main()