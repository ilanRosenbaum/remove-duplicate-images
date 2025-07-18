# Ilan's Website
# Copyright (C) 2024-2025 ILAN ROSENBAUM
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.


import os
import argparse

def set_creation_date_to_modified_date(file_path):
    """
    Set the creation date of the file to its last modified date.
    We do this because when porting photos from phone to computer, the creation date is set to the date of the transfer. but the modified date is preserved.
    """
    modified_time = os.path.getmtime(file_path)
    os.utime(file_path, (modified_time, modified_time))  # Set both atime and mtime to modified_time


def process_directory(directory):
    """
    Process all files in the given directory and its subdirectories.
    """
    files_updated = 0

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            set_creation_date_to_modified_date(file_path)
            files_updated += 1
            print(f"Updated: {file_path}")
    
    return files_updated

def main():
    parser = argparse.ArgumentParser(description='Update file creation date to match modified date for all files in a directory')
    parser.add_argument('path', type=str, help='Path to the directory containing the files')
    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"Error: The path {args.path} does not exist.")
        return

    files_updated = process_directory(args.path)
    print(f'Process completed {files_updated} files updated.')

if __name__ == "__main__":
    main()
