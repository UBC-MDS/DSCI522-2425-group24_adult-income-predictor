"""
read_and_validate.py

Author: Michael Suriawan
Date: 2024-12-4

This script reads a raw data file, validates it against defined schema rules,
logs validation errors, and outputs the cleaned data for further processing.

Key Features:
1. Validate file existence and format.
2. Validate data against a strict schema using `pandera`.
3. Log validation errors to a file.
4. Save the cleaned data to a specified directory.

Dependencies:
- pandas
- pandera
- click
- json
- os
- logging
"""

import os
import json
import click
import pandas as pd
import pandera as pa
import logging

@click.command()
@click.option('--raw_dir', type=str, help="Path to raw data")
@click.option('--processor_dir', type=str, help="Path to directory where processed data will be written to")
def main(raw_dir, processor_dir):
    """
    Main function for reading and validating raw data.

    Parameters:
    - raw_dir (str): Path to the raw data file.
    - processor_dir (str): Directory to save the processed data.
    """

    # Step 1: Validate raw data file
    if not os.path.exists(raw_dir):
        raise FileNotFoundError(f"Unable to find raw file in {raw_dir}. Please check the download step.")
    if not raw_dir.endswith('.data'):
        raise ValueError(f"{raw_dir} is not a DATA file. Please ensure the correct file format.")
    print("Data Validation 1 passed: File existence and format verified.")

    # Step 2: Read data into a DataFrame
    col_names = [
        'age', 'workclass', 'fnlwgt', 'education', 'education-num',
        'marital-status', 'occupation', 'relationship', 'race', 'sex',
        'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'income'
    ]
    data_adult = pd.read_csv(raw_dir, names=col_names)

    # Step 3: Configure logging for validation errors
    # Create the directory if it doesn't exist
    if not os.path.isdir("data/logs"):
        os.makedirs("data/logs", exist_ok=True)

    logging.basicConfig(
        filename="data/logs/validation_errors.log",
        filemode="w",
        format="%(asctime)s - %(message)s",
        level=logging.INFO,
    )

    # Step 4: Define the validation schema
    schema = pa.DataFrameSchema(
        {
            "age": pa.Column(int, pa.Check.between(0, 120), nullable=True),
            "workclass": pa.Column(str, pa.Check.isin([
                "Private", "Self-emp-not-inc", "Self-emp-inc", "Federal-gov",
                "Local-gov", "State-gov", "Without-pay", "Never-worked"
            ]), nullable=True),
            "fnlwgt": pa.Column(int, nullable=True),
            "education": pa.Column(str, pa.Check.isin([
                "Bachelors", "Some-college", "11th", "HS-grad", "Prof-school",
                "Assoc-acdm", "Assoc-voc", "9th", "7th-8th", "12th", "Masters",
                "1st-4th", "10th", "Doctorate", "5th-6th", "Preschool"
            ]), nullable=True),
            "education-num": pa.Column(int, pa.Check.between(0, 50), nullable=True),
            "marital-status": pa.Column(str, pa.Check.isin([
                "Married-civ-spouse", "Divorced", "Never-married", "Separated",
                "Widowed", "Married-spouse-absent", "Married-AF-spouse"
            ]), nullable=True),
            "occupation": pa.Column(str, pa.Check.isin([
                "Tech-support", "Craft-repair", "Other-service", "Sales", 
                "Exec-managerial", "Prof-specialty", "Handlers-cleaners", 
                "Machine-op-inspct", "Adm-clerical", "Farming-fishing", 
                "Transport-moving", "Priv-house-serv", "Protective-serv", 
                "Armed-Forces"
            ]), nullable=True),
            "relationship": pa.Column(str, pa.Check.isin([
                "Wife", "Own-child", "Husband", "Not-in-family", 
                "Other-relative", "Unmarried"
            ]), nullable=True),
            "race": pa.Column(str, pa.Check.isin([
                "White", "Asian-Pac-Islander", "Amer-Indian-Eskimo", 
                "Other", "Black"
            ]), nullable=True),
            "sex": pa.Column(str, pa.Check.isin(["Female", "Male"]), nullable=True),
            "capital-gain": pa.Column(int, nullable=True),
            "capital-loss": pa.Column(int, nullable=True),
            "hours-per-week": pa.Column(int, pa.Check.between(0, 120), nullable=True),
            "native-country": pa.Column(str, pa.Check.isin([
                "United-States", "Cambodia", "England", "Puerto-Rico", "Canada", 
                "Germany", "Outlying-US(Guam-USVI-etc)", "India", "Japan", 
                "Greece", "South", "China", "Cuba", "Iran", "Honduras", 
                "Philippines", "Italy", "Poland", "Jamaica", "Vietnam", 
                "Mexico", "Portugal", "Ireland", "France", 
                "Dominican-Republic", "Laos", "Ecuador", "Taiwan", 
                "Haiti", "Columbia", "Hungary", "Guatemala", "Nicaragua", 
                "Scotland", "Thailand", "Yugoslavia", "El-Salvador", 
                "Trinadad&Tobago", "Peru", "Hong", "Holand-Netherlands"
            ]), nullable=True),
            "income": pa.Column(str, pa.Check.isin([">50K", "<=50K"]), nullable=True)
        },
        checks=[
            pa.Check(lambda df: ~df.duplicated().any(), error="Duplicate rows found."),
            pa.Check(lambda df: ~(df.isna().all(axis=1)).any(), error="Empty rows found."),
        ],
    )

    # Step 5: Validate the data
    # Initialize error cases DataFrame
    error_cases = pd.DataFrame()
    data = data_adult.copy()

    # Validate data and handle errors
    try:
        validated_data = schema.validate(data, lazy=True)
    except pa.errors.SchemaErrors as e:
        error_cases = e.failure_cases

        # Convert the error message to a JSON string
        error_message = json.dumps(e.message, indent=2)
        logging.error("\n" + error_message)

    # Filter out invalid rows based on the error cases
    if not error_cases.empty:
        invalid_indices = error_cases["index"].dropna().unique()
        validated_data = data
        validated_data.drop(index=invalid_indices)
        validated_data = validated_data.reset_index(drop=True)
        validated_data = validated_data.drop_duplicates()
        validated_data = validated_data.dropna(how="all")
    else:
        validated_data = data

    print("Data Validation 2 passed: Dataframe validated successfully.")

    # Step 6: Save validated data
    # Create the directory if it doesn't exist
    if not os.path.isdir(processor_dir):
        os.makedirs(processor_dir, exist_ok=True)

    output_file = os.path.join(processor_dir, "cleaned_data.csv")
    validated_data.to_csv(output_file, index=False)
    print(f"Cleaned data saved to {output_file}")


if __name__ == '__main__':
    main()
    