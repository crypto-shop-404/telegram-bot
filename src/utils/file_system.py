import os
import pathlib
import shutil


def delete_dir(path: str | pathlib.Path):
    if os.path.exists(path):
        os.rmdir(path)


def delete_file(path: str | pathlib.Path):
    if os.path.exists(path):
        os.remove(path)


def move_file(path: str | pathlib.Path, destination_path: str | pathlib.Path):
    if os.path.exists(path):
        return shutil.move(path, destination_path)
