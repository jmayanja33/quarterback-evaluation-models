import os


def make_directory(filepath, directory=None):
    """Function to make a directory if it does not already exist"""
    if directory is not None:
        dir_path = os.path.join(filepath, directory)
    else:
        dir_path = filepath

    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
