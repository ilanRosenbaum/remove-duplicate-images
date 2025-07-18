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

        # Verify no file that includes "copy" in its filename remains and that the right amount of files remain
        file_count = 0
        for _, _, files in os.walk(base_path):
            for file in files:
                self.assertNotIn('copy', file)
                if file != '.DS_Store':
                    file_count += 1
        
        self.assertEqual(file_count, 4)        

if __name__ == '__main__':
    unittest.main()