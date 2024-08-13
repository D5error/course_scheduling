import os


def make_file(path):
    if not os.path.exists(path):
        os.makedirs(path)
