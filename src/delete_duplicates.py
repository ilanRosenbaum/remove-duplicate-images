# src/delete_duplicates.py

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
    if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        return get_image_phash(file_path)
    elif file_path.lower().endswith(('.mp4', '.mov')):
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

        # Example: choose a frame from the beginning, middle, and end
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
    """

    files_removed = 0
    hashes = {}
    for folder_subpath, folder_priority in folders.items():
        folder_path = os.path.join(base_path, folder_subpath)
        if not os.path.exists(folder_path):
            print(f"Folder not found: {folder_path}")
            continue

        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_hash_with_priority = [get_media_phash(file_path), folder_priority, file_path]

                if file_hash_with_priority[0] is None:
                    continue

                if file_hash_with_priority[0] not in hashes.keys():
                    # If a picture or video with the same hash doesn't exist, add it to the dictionary
                    hashes[file_hash_with_priority[0]] = [file_hash_with_priority[1], file_hash_with_priority[2]]      
                elif file_hash_with_priority[1] < hashes[file_hash_with_priority[0]][0]:
                    # If a picture or video with the same hash exists, but the new one has a higher priority, remove the old one
                    os.remove(hashes[file_hash_with_priority[0]][1])
                    files_removed += 1
                    hashes[file_hash_with_priority[0]] = [file_hash_with_priority[1][0], file_path]
                else:
                    # If a picture or video with the same hash exists, but the old one has a higher priority, remove the new one
                    os.remove(file_path)
                    files_removed += 1

    return files_removed

def main():
    """
    Process images and videos to remove duplicates.
    """
    parser = argparse.ArgumentParser(description="Process images and videos to remove duplicates.")
    parser.add_argument('base_path', type=str, help='Base path for the folders')
    parser.add_argument('folders', type=json.loads, help='JSON string representing the folder dictionary with priorities')
    args = parser.parse_args()

    base_path = args.base_path
    priority_folders = args.folders

    files_removed = populate_and_remove_duplicates(base_path, priority_folders)
    print(f"Removed {files_removed} files")

if __name__ == "__main__":
    main()
