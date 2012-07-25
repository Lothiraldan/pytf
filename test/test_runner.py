import unittest
import sys

try:
    from unittest.mock import Mock, sentinel, call
except ImportError:
    from mock import Mock, sentinel, call

from os.path import join, dirname

from utils import FakeModule, FunctionMock, LoaderMock
from pytf import TestRunner, TestFinder, TestLoader, TestExecutor, Test


class TestTestRunner(unittest.TestCase):
    '''The rule is try to call each loader by descending level and as soon as
    one loader return a test, take it and iterate over next variables.
    '''

    def setUp(self):
        self.module_object = sentinel.OBJECT
        self.module = FakeModule({'obj': self.module_object})

    def test_set_loaders(self):
        loader1 = LoaderMock()
        loader1.level = 0

        loader2 = LoaderMock()
        loader2.level = 10

        runner = TestRunner(None, loaders=[])
        runner.set_loaders([loader1, loader2])
        self.assertEquals(dict(runner.loaders), {0: [loader1], 10: [loader2]})

    def test_loaders(self):
        loader1 = LoaderMock()
        loader1.load_object.return_value = None

        loader2 = LoaderMock()
        loader2.load_object.return_value = None

        loaders = {0: [loader1, loader2]}

        runner = TestRunner(None)
        runner.loaders = loaders
        runner._load_modules([self.module])

        for loader_mock in loaders[0]:
            self.assertEquals(loader_mock.load_object.call_args_list,
                [call(self.module_object, self.module)])

    def test_loaders_first_response(self):
        '''Second loader should not been called has first loader always return
        a test for each object of module
        '''

        good_loader = LoaderMock()
        good_loader.load_object.return_value = [sentinel.TEST]

        other_loader = LoaderMock()
        other_loader.load_object.return_value = None

        loaders = {0: [good_loader, other_loader]}

        runner = TestRunner(None)
        runner.loaders = loaders
        tests = runner._load_modules([self.module])

        self.assertEquals(tests, [sentinel.TEST])

        self.assertEquals(good_loader.load_object.call_args_list,
            [call(self.module_object, self.module)])

        self.assertFalse(other_loader.load_object.called)

    def test_loaders_multiple_level(self):
        '''Loader of level 0 should not been called
        '''

        level1_loader = LoaderMock()
        level1_loader.load_object.return_value = [sentinel.TEST]

        level0_loader = LoaderMock()
        level0_loader.load_object.return_value = [sentinel.TEST]

        loaders = {1: [level1_loader], 0: [level0_loader]}

        runner = TestRunner(None)
        runner.loaders = loaders
        runner._load_modules([self.module])

        self.assertEquals(level1_loader.load_object.call_args_list,
            [call(self.module_object, self.module)])

        self.assertFalse(level0_loader.load_object.called)

    def test_build_test_suite(self):
        function_mock = FunctionMock(Mock())
        fake_module = FakeModule({'test': function_mock})
        sys.modules[fake_module.__name__] = fake_module

        mock_finder = Mock()
        mock_finder.find.return_value = ['%s.py' % fake_module.__name__]
        finders = [mock_finder]

        loader = TestLoader()
        loaders = [loader]

        runner = TestRunner(finders, loaders)
        test_suite = runner._build_test_suite()

        self.assertEquals(test_suite, [Test('fake_module.call', function_mock)])

        del sys.modules[fake_module.__name__]


class TestTestRunnerFullChainTC(unittest.TestCase):
    def test_full_process(self):
        finders = [TestFinder(join(dirname(__file__),
            'test_finder_dirs/test_full_chain/'))]
        loaders = [TestLoader()]
        mock_reporter = Mock()
        reporters = [mock_reporter]
        executor = TestExecutor(reporters)

        runner = TestRunner(finders, loaders, executor)
        runner.run()

        self.assertEquals(mock_reporter.show_result.call_count, 1)
