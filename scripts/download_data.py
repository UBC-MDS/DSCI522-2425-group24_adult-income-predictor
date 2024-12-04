# download_data.py
# author: Michael Suriawan
# date: 2024-12-4

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
    """
    request = requests.get(url)
    filename_from_url = os.path.basename(url)

    # check if URL exists, if not raise an error
    if request.status_code != 200:
        raise ValueError('The URL provided does not exist.')
    
    # check if the URL points to a zip file, if not raise an error  
    if filename_from_url[-4:] != '.zip':
        raise ValueError('The URL provided does not point to a zip file.')
    
    # check if the directory exists, if not create that directory
    if not os.path.isdir(directory):
        os.makedirs(directory, exist_ok = True)

    # write the zip file to the directory
    path_to_zip_file = os.path.join(directory, filename_from_url)
    with open(path_to_zip_file, 'wb') as f:
        f.write(request.content)

    # Extract the zip file into the directory
    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_ref.extractall(directory)

    # Print success message!
    print(f"Succesfully downloaded data to: {directory}")


@click.command()
@click.option('--url', type=str, help="URL of dataset to be downloaded")
@click.option('--target_dir', type=str, help="Path to directory where raw data will be written to")
def main(url, target_dir):
    """Downloads data zip data from the web to a local filepath and extracts it."""
    try:
        read_zip(url, target_dir)
    except Exception as e:
        print(f"An error has occurred: {e}")


if __name__ == '__main__':
    main()
