import os


def make_directory(filepath, directory):
    """Function to make a directory if it does not already exist"""
    dir_path = os.path.join(filepath, directory)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
