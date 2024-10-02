#!/usr/bin/env python3
import argparse
import zipfile
import os
from datetime import datetime
from colorama import Fore, Style
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


def zipdir(directory, zip_file, formats):
    excludes = []
    for root, _, files in os.walk(directory):
        level = root.replace(directory, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print(Fore.BLUE+'{}{}/'.format(indent,
              os.path.basename(root)) + Style.RESET_ALL)
        subindent = ' ' * 4 * (level + 1)
        for file in files:
            if os.path.splitext(file)[1] not in formats:
                print(Fore.LIGHTCYAN_EX +
                      '{}{}'.format(subindent, file) + Style.RESET_ALL)
                file_path = os.path.join(root, file)
                zip_file.write(file_path, arcname=os.path.relpath(
                    file_path, start=directory))
            else:
                excludes.append(file)
    return excludes


if __name__ == '__main__':
    args = parse_arguments()
    excludeFormats = args.exclude if args.exclude else []
    try:
        validate(Path(args.path))
    except FileNotFoundError as e:
        print(Fore.RED + "ERROR: " + Fore.WHITE + f"{e}")
    date = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    with zipfile.ZipFile(f'backup_{date}.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        excludes = zipdir(args.path, zipf, excludeFormats)
    print("Excluded files:")
    for file in excludes:
        print(Fore.LIGHTRED_EX + file)
