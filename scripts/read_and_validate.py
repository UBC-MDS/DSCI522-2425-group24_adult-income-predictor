# read_and_validate.py
# author: Michael Suriawan
# date: 2024-12-4

import os
import click
import pandas as pd
import pandera as pa
import src.create_dir_and_file_if_not_exist as create_dir_and_file_if_not_exist
import src.validate_df as validate_df
import src.validate_raw_file as validate_raw_file


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
    validate_raw_file(raw_dir)
    print("Data Validation 1 passed: File existence and format verified.")

    # Step 2: Read data into a DataFrame
    col_names = [
        'age', 'workclass', 'fnlwgt', 'education', 'education-num',
        'marital-status', 'occupation', 'relationship', 'race', 'sex',
        'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'income'
    ]
    data_adult = pd.read_csv(raw_dir, names=col_names)

    # Step 3: Validate data frame
    validated_data = validate_df(data_adult)
    print("Data Validation 2 passed: Dataframe validated successfully.")

    # Step 4: Save validated data
    output_file = create_dir_and_file_if_not_exist(processor_dir, "cleaned_data.csv")
    validated_data.to_csv(output_file, index=False)
    print(f"Cleaned data saved to {output_file}")


if __name__ == '__main__':
    main()