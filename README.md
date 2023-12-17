# Purpose
I wanted to have all the images in my google photos on my device without having duplicates while maintaining my folder structure. This turned out to be much more difficult than anticipated. I used Google takeout to get my photos (used a different program to merge JSON files with photos) but now I needed a way to merge my google photos that don't have my local folder structure and my local photos while removing all duplicates.

This is difficult because google compresses the files in such a way where they have differnt metadata and file size to the originals. My solution was to put all of the google photos files in one folder, port all my photos with folder structure from my phone to my computer, then use pHash to identity which photos look similar. Once we identity a photo already exists we consult a priority list of the folders. I chose to do it this way as if I photo exists in two folders, for example "food" and "camera" I want to retain the one inside food as that one that has already been organized. But if a file is in "camera" and "archive" I want to keep the photo in archive.

Videos are handeled by grabing the first middle and last frame from a video, using pHash on all 3 and comparing those 3 values to all other video values.

This entire script is wildly inefficent, if you have potential improvements they would be greatly apreciated, but given this only needed to work on time for me speed wasn't my priority.  

# Prerequisites
Python >= 3.7.4
- opencv-python
  - install with `pip install opencv-python`
- Pillow
  - Install with `pip install Pillow`
# Instructions
Create priority dictionary for subfolders of your media (ie {"folder1": 1, "folder2": 2}) where higher number is lower priority. If duplicates are found the file(s) deleted will be from the lower priority folder.

Run python script with priority dictionary and path to photos as arguments: 
`python delete_duplicates.py "/path/to/your/photos" '{"folder1": 1, "folder2": 2}'`
