# download_data.py
# author: Michael Suriawan
# date: 2024-12-4

import sys
import os
import click
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.read_zip import read_zip

@click.command()
@click.option('--url', type=str, required=True, help="URL of the dataset to be downloaded (must be a ZIP file).")
@click.option('--target_dir', type=str, required=True, help="Path to the directory where the data will be stored.")
def main(url, target_dir):
    """
    Command-line interface for downloading and extracting downloaded files.

    Parameters:
    ----------
    url : str
        The URL of the ZIP file to download.
    target_dir : str
        The directory to save and extract the contents of the downloaded file.

    Returns:
    -------
    None
    """
    try:
        read_zip(url, target_dir)
    except Exception as e:
        print(f"An error has occurred: {e}")


if __name__ == '__main__':
    main()
    