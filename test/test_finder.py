import unittest

from os.path import join, dirname

from pytf import TestFinder


class TestFinderTestCase(unittest.TestCase):

    def test_simple_directory(self):
        finder = TestFinder(join(dirname(__file__),
            'test_finder_dirs/test_dir_1/'))
        self.assertItemsEqual(finder.find(),
            [join(dirname(__file__),
                'test_finder_dirs/test_dir_1/test_simple.py')])

    def test_sub_directory(self):
        finder = TestFinder(join(dirname(__file__),
            'test_finder_dirs/test_dir_2/'))
        self.assertItemsEqual(finder.find(),
            [join(dirname(__file__),
                'test_finder_dirs/test_dir_2/test_simple.py'),
             join(dirname(__file__),
                'test_finder_dirs/test_dir_2/subdir/test_simple.py')])

    def test_no_package(self):
        finder = TestFinder(join(dirname(__file__),
            'test_finder_dirs/test_dir_3/'))
        self.assertItemsEqual(finder.find(),
            [join(dirname(__file__),
                'test_finder_dirs/test_dir_3/test_simple.py')])

    def test_default_finder_rgx(self):
        finder = TestFinder(join(dirname(__file__),
            'test_finder_dirs/test_dir_4/'))
        self.assertItemsEqual(finder.find(),
            [join(dirname(__file__),
                'test_finder_dirs/test_dir_4/test_simple.py')])

if __name__ == "__main__":
    unittest.main()
