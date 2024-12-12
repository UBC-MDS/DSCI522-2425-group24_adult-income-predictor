import os


def create_dir_and_file_if_not_exist(directory, filename):    
    """
    Create a directory and file specified in filename if it does not exist already.

    Parameters:
    ----------
    directory : str
        The directory where the contents of the zip file will be extracted.
    filename: str
        name of the file that will be included, along with its format

    Returns:
    -------
    path to the newly created file
    """
    if not os.path.isdir(directory):
        os.makedirs(directory, exist_ok=True)
        
    path_to_zip_file = os.path.join(directory, filename)
    return path_to_zip_file