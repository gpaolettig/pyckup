#!/usr/bin/env python3
import argparse
import zipfile
import os
from datetime import datetime
from pathlib import Path


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Simple python script for backups. Author @gpaolettig")
    parser.add_argument('path', help='path or directory to backup')
    parser.add_argument('--exclude', nargs='+', help='file formats to exclude')
    return parser.parse_args()


def validate(path):
    if not path.exists():
        raise FileNotFoundError(f"File o directory {path} doesn't exists")


def print_directory_tree(directory, root, level, is_directory):
    indent = ' ' * 4 * (level)
    if is_directory:
        print(f"{indent}{os.path.basename(root)}/")
    else:
        subindent = ' ' * 4 * (level + 1)
        print(f"{subindent}{root}")


def zipdir(directory, zip_file, formats):
    excludes = []
    for root, _, files in os.walk(directory):
        level = root.replace(directory, '').count(os.sep)
        print_directory_tree(directory, root, level, is_directory=True)
        for file in files:
            if os.path.splitext(file)[1] not in formats:
                print_directory_tree(
                    directory, file, level, is_directory=False)
                file_path = os.path.join(root, file)
                zip_file.write(file_path, arcname=os.path.relpath(
                    file_path, start=directory))
            else:
                excludes.append(file)
    return excludes


def print_excludes(excludes):
    print("Excluded files:")
    for file in excludes:
        print(file)


def create_zip():
    date = datetime.now().strftime("%Y-%m-%d:%H-%M-%S")
    with zipfile.ZipFile(f'backup_{date}.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        excludes = zipdir(args.path, zipf, excludeFormats)
    return excludes 

if __name__ == '__main__':
    args = parse_arguments()
    excludeFormats = args.exclude if args.exclude else []
    try:
        validate(Path(args.path))
    except FileNotFoundError as e:
        print("ERROR: " + f"{e}")
    print_excludes(create_zip())
