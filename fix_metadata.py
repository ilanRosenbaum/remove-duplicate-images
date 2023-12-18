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
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            set_creation_date_to_modified_date(file_path)
            print(f"Updated: {file_path}")

def main():
    parser = argparse.ArgumentParser(description='Update file creation date to match modified date for all files in a directory')
    parser.add_argument('path', type=str, help='Path to the directory containing the files')
    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"Error: The path {args.path} does not exist.")
        return

    process_directory(args.path)
    print("Process completed.")

if __name__ == "__main__":
    main()
