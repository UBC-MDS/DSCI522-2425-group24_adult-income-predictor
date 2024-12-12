import os


def validate_raw_file(raw_dir):
    """
    Validates the raw file.

    Parameters
    ----------
    raw file: str
        The directory to the raw file being validated.
    """
    if not os.path.exists(raw_dir):
        raise FileNotFoundError(f"Unable to find raw file in {raw_dir}. Please check the download step.")
    if not raw_dir.endswith('.data'):
        raise ValueError(f"{raw_dir} is not a DATA file. Please ensure the correct file format.")