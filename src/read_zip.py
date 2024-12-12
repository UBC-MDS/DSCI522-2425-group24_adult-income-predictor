import os
import requests
import zipfile
import src.create_dir_and_file_if_not_exist as create_dir_and_file_if_not_exist


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
    
    # Save the ZIP file to the target directory
    path_to_zip_file = create_dir_and_file_if_not_exist(directory, filename_from_url)
    with open(path_to_zip_file, 'wb') as f:
        f.write(request.content)

    # Extract the contents of the ZIP file
    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_ref.extractall(directory)

    # Print success message
    print(f"Successfully downloaded and extracted data to: {directory}")