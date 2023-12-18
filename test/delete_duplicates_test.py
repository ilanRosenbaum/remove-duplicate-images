# scripts/test.py

import unittest
import os
import shutil
from src.delete_duplicates import populate_and_remove_duplicates

class TestRemoveDuplicates(unittest.TestCase):
    def setUp(self):
        # Copy test test/data
        shutil.copytree('test/data/identical_photos', 'test/data/tmp/copy_photos')
        shutil.copytree('test/data/identical_videos', 'test/data/tmp/copy_videos')

    def tearDown(self):
        # Clean up new test/data
        shutil.rmtree('test/data/tmp/copy_photos')
        shutil.rmtree('test/data/tmp/copy_videos')

    def test_remove_duplicates(self):
        base_path = 'test/data/tmp/'
        folders = {'copy_photos/high_priority': 1, 'copy_photos/low_priority': 2, 'copy_videos/high_priority': 3, 'copy_videos/low_priority': 4}

        populate_and_remove_duplicates(base_path, folders)

        # Verify no file that includes "copy" in its filename remains
        for _, _, files in os.walk(base_path):
            for file in files:
                self.assertNotIn('copy', file)

if __name__ == '__main__':
    unittest.main()