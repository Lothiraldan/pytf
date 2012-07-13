import unittest

from pytf import TestFinder


class TestFinderTestCase(unittest.TestCase):

    def test_simple_directory(self):
        finder = TestFinder('./test_finder_dirs/test_dir_1/')
        self.assertItemsEqual(finder._find_test_files(),
            ['./test_finder_dirs/test_dir_1/test_simple.py'])

    def test_sub_directory(self):
        finder = TestFinder('./test_finder_dirs/test_dir_2/')
        self.assertItemsEqual(finder._find_test_files(),
            ['./test_finder_dirs/test_dir_2/test_simple.py',
             './test_finder_dirs/test_dir_2/subdir/test_simple.py'])

if __name__ == "__main__":
    unittest.main()
