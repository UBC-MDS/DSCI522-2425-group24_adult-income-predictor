"""
Script for downloading and extracting datasets from the web.

This script takes a URL pointing to a ZIP file and a target directory as inputs.
It downloads the ZIP file, saves it to the target directory, and extracts its contents.
Useful for automating the process of retrieving datasets for data analysis or machine learning projects.

Usage:
------
Run the script from the command line:
    python download_data.py --url <URL> --target_dir <DIRECTORY>

Dependencies:
-------------
- click
- os
- zipfile
- requests

Author:
-------
Michael Suriawan

Date:
-----
2024-12-4
"""

import click
import os
import zipfile
import requests


def read_zip(url, directory):
    """
    Read a zip file from the given URL and extract its contents to the specified directory.

    Parameters:
    ----------
    url : str
        The URL of the zip file to be read.
    directory : str
        The directory where the contents of the zip file will be extracted.

    Returns:
    -------
    None

    Raises:
    ------
    ValueError:
        If the URL is invalid or does not point to a ZIP file.
    """
    # Send an HTTP GET request to the URL
    request = requests.get(url)
    filename_from_url = os.path.basename(url)

    # Check if the URL is accessible
    if request.status_code != 200:
        raise ValueError("The URL provided does not exist.")
    
    # Ensure the URL points to a ZIP file
    if not filename_from_url.endswith('.zip'):
        raise ValueError("The URL provided does not point to a ZIP file.")
    
    # Create the directory if it doesn't exist
    if not os.path.isdir(directory):
        os.makedirs(directory, exist_ok=True)

    # Save the ZIP file to the target directory
    path_to_zip_file = os.path.join(directory, filename_from_url)
    with open(path_to_zip_file, 'wb') as f:
        f.write(request.content)

    # Extract the contents of the ZIP file
    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_ref.extractall(directory)

    # Print success message
    print(f"Successfully downloaded and extracted data to: {directory}")


@click.command()
@click.option('--url', type=str, required=True, help="URL of the dataset to be downloaded (must be a ZIP file).")
@click.option('--target_dir', type=str, required=True, help="Path to the directory where the data will be stored.")
def main(url, target_dir):
    """
    Command-line interface for downloading and extracting ZIP files.

    Parameters:
    ----------
    url : str
        The URL of the ZIP file to download.
    target_dir : str
        The directory to save and extract the contents of the ZIP file.

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
    