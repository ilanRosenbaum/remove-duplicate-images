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
import imagehash
from PIL import Image
import cv2
import json
import argparse


def get_image_phash(image_path):
    """
    Get the phash of an image.
    """
    try:
        img = Image.open(image_path)
        return imagehash.phash(img)
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        return None


def get_media_phash(file_path: str):
    """
    Get the phash of an image or video.
    """
    if file_path.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        return get_image_phash(file_path)
    elif file_path.lower().endswith((".mp4", ".mov")):
        return get_video_phash(file_path)
    else:
        return None


def get_video_phash(video_path: str):
    """
    Get the phash of a video.
    """
    try:
        cap = cv2.VideoCapture(video_path)
        frames = []
        success, image = cap.read()
        while success:
            frames.append(image)
            success, image = cap.read()

        # choose a frame from the beginning, middle, and end
        key_frames = [frames[0], frames[len(frames) // 2], frames[-1]]
        frame_hashes = [imagehash.phash(Image.fromarray(frame)) for frame in key_frames]

        return tuple(frame_hashes)
    except Exception as e:
        print(f"Error processing video {video_path}: {e}")
        return None


def populate_and_remove_duplicates(base_path, folders: dict):
    """
    Populate a dictionary with the phashes of all files in the given folders,
    then remove all duplicate images and videos that are not in the priority folders.
    Tracks removals per top-level folder (relative to the base path).
    """
    total_removed = 0
    removed_counts = {}  # key: top-level folder name, value: count removed
    hashes = {}

    # Helper function to update the removed_counts dict
    def record_removal(file_path):
        nonlocal total_removed
        # Determine the top-level folder relative to base_path
        rel_folder = os.path.relpath(file_path, base_path).split(os.sep)[0]
        removed_counts[rel_folder] = removed_counts.get(rel_folder, 0) + 1
        total_removed += 1

    for folder_subpath, folder_priority in folders.items():
        folder_path = os.path.join(base_path, folder_subpath)
        if not os.path.exists(folder_path):
            print(f"Folder not found: {folder_path}")
            continue

        print(f"Processing folder: {folder_path}")
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                media_hash = get_media_phash(file_path)
                if media_hash is None:
                    continue

                file_data = [media_hash, folder_priority, file_path]

                if media_hash not in hashes:
                    # New file; add it to the dictionary.
                    hashes[media_hash] = [folder_priority, file_path]
                elif file_data[1] < hashes[media_hash][0]:
                    # The new file has higher priority.
                    # Remove the existing file.
                    old_file_path = hashes[media_hash][1]
                    try:
                        os.remove(old_file_path)
                        record_removal(old_file_path)
                    except Exception as e:
                        print(f"Error removing file {old_file_path}: {e}")
                    # Update with the new file.
                    hashes[media_hash] = [file_data[1], file_path]
                else:
                    # Existing file has higher priority; remove the new file.
                    try:
                        os.remove(file_path)
                        record_removal(file_path)
                    except Exception as e:
                        print(f"Error removing file {file_path}: {e}")

    return removed_counts, total_removed


def main():
    """
    Process images and videos to remove duplicates.
    """
    parser = argparse.ArgumentParser(
        description="Process images and videos to remove duplicates."
    )
    parser.add_argument("base_path", type=str, help="Base path for the folders")
    parser.add_argument(
        "folders",
        type=json.loads,
        help="JSON string representing the folder dictionary with priorities",
    )
    args = parser.parse_args()

    base_path = args.base_path
    priority_folders = args.folders

    removed_counts, total_removed = populate_and_remove_duplicates(
        base_path, priority_folders
    )

    # Print removal count for each folder
    for folder, count in removed_counts.items():
        print(f"{folder}: {count} removed")

    print("")  # New line
    print(f"Removed {total_removed} duplicate files total")


if __name__ == "__main__":
    main()
