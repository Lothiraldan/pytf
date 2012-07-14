import unittest

try:
    from unittest.mock import Mock, sentinel, call
except ImportError:
    from mock import Mock, sentinel, call

from utils import FakeModule
from pytf import TestRunner


class TestTestRunner(unittest.TestCase):

    def setUp(self):
        self.module_object = sentinel.OBJECT
        self.module = FakeModule({'obj': self.module_object})

    def test_loaders(self):
        loader1 = Mock()
        loader1.load_object.return_value = None

        loader2 = Mock()
        loader2.load_object.return_value = None

        loaders = {0: [loader1, loader2]}

        runner = TestRunner()
        runner.set_loaders(loaders)
        runner._load_modules([self.module])

        for loader_mock in loaders[0]:
            self.assertEquals(loader_mock.load_object.call_count, 1)
            self.assertEquals(loader_mock.load_object.call_args_list,
                [call(self.module_object)])

    def test_loaders_first_response(self):
        '''Second loader should not been called has first loader always return
        a test for each object of module
        '''

        good_loader = Mock()
        good_loader.load_object.return_value = sentinel.TEST

        other_loader = Mock()
        other_loader.load_object.return_value = None

        loaders = {0: [good_loader, other_loader]}

        runner = TestRunner()
        runner.set_loaders(loaders)
        runner._load_modules([self.module])

        self.assertEquals(good_loader.load_object.call_count, 1)
        self.assertEquals(good_loader.load_object.call_args_list,
            [call(self.module_object)])

        self.assertFalse(other_loader.load_object.called)

    def test_loaders_multiple_level(self):
        '''Loader of level 0 should not been called
        '''

        level1_loader = Mock()
        level1_loader.load_object.return_value = sentinel.TEST

        level0_loader = Mock()
        level0_loader.load_object.return_value = sentinel.TEST

        loaders = {1: [level1_loader], 0: [level0_loader]}

        runner = TestRunner()
        runner.set_loaders(loaders)
        runner._load_modules([self.module])

        self.assertEquals(level1_loader.load_object.call_count, 1)
        self.assertEquals(level1_loader.load_object.call_args_list,
            [call(self.module_object)])

        self.assertFalse(level0_loader.load_object.called)
