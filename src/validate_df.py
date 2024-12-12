import logging
import json
import pandas as pd
import pandera as pa
import create_dir_and_file_if_not_exist


def validate_df(adult_income_dataframe):
    """
    Validates the adult income dataframe.

    Parameters
    ----------
    adult_income_dataframe : pandas.DataFrame
        The DataFrame containing adult income dataframe with the columns: 
        'age', 'workclass', 'fnlwgt', 'education', 'education-num',
        'marital-status', 'occupation', 'relationship', 'race', 'sex',
        'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'income'.

    Returns
    -------
    pandas.DataFrame
        The validated DataFrame that conforms to the specified schema.
    """
    
    # Setup validation_errors.log file
    validation_error_log_dir = create_dir_and_file_if_not_exist("data/logs", "validation_errors.log")
    logging.basicConfig(
        filename=validation_error_log_dir,
        filemode="w",
        format="%(asctime)s - %(message)s",
        level=logging.INFO,
    )

    # schema
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
 
    # Initialize error cases DataFrame
    error_cases = pd.DataFrame()
    data = adult_income_dataframe.copy()

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

    return validated_data