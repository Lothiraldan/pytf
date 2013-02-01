import unittest

try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

from pytf import TestLoader
from pytf.dataprovider import DataProvider, call
from utils import (FunctionMock, MockTest, FakeModule)


class DataProviderTestCase(unittest.TestCase):

    def test_data_provider_function(self):
        mock = Mock()
        function_mock = FunctionMock(mock)

        tests = {'call1': call(1, arg=2), 'call2': call(2, arg=3), 'call3':
            call(3, arg=4)}
        DataProvider(**tests)(function_mock)

        loader = TestLoader()
        test_suite = list(loader.load_object(function_mock, FakeModule({})))

        self.assertEquals(len(test_suite), len(tests))

        for test in test_suite:
            test()

        self.assertEquals(mock.call_args_list, tests.values())

    def test_data_provider_method(self):
        fake_test_case = MockTest()
        fake_module = FakeModule({})

        tests = {'call1': call(1, arg=2), 'call2': call(2, arg=3), 'call3':
            call(3, arg=4)}
        DataProvider(**tests)(fake_test_case.__dict__['test_test'])

        loader = TestLoader()
        test_suite = list(loader.load_object(fake_test_case, fake_module))

        self.assertEquals(len(test_suite), len(tests))

        for test in test_suite:
            test()

        self.assertEquals(fake_test_case.set_up_mock.call_count, len(tests))
        self.assertEquals(fake_test_case.test_mock.call_args_list, tests.values())
        self.assertEquals(fake_test_case.tear_down_mock.call_count, len(tests))

    def test_data_provider_class(self):
        fake_test_case = MockTest()
        fake_module = FakeModule({})

        tests = {'call1': call(1, arg=2), 'call2': call(2, arg=3), 'call3':
            call(3, arg=4)}
        DataProvider(**tests)(fake_test_case)

        loader = TestLoader()
        test_suite = list(loader.load_object(fake_test_case, fake_module))

        self.assertEquals(len(test_suite), len(tests))

        for test in test_suite:
            test()

    def test_data_provider_class_and_method(self):
        fake_test_case = MockTest()
        fake_module = FakeModule({})

        class_tests = {'call1': call(1, arg=2), 'call2': call(2, arg=3), 'call3':
            call(3, arg=4)}
        DataProvider(**class_tests)(fake_test_case)

        method_tests = {'call4': call(4, arg=5), 'call5': call(5, arg=6),
            'call6': call(6, arg=7)}
        DataProvider(**method_tests)(fake_test_case.__dict__['test_test'])

        loader = TestLoader()
        test_suite = list(loader.load_object(fake_test_case, fake_module))

        self.assertEquals(len(test_suite), len(class_tests) * len(method_tests))

        for test in test_suite:
            test()

    def test_data_provider_function_messages(self):
        mock = Mock()
        function_mock = FunctionMock(mock)

        tests = {'call1': call(1, arg=2), 'call2': call(2, arg=3), 'call3':
            call(3, arg=4)}
        DataProvider(**tests)(function_mock)

        loader = TestLoader()
        test_suite = list(loader.load_object(function_mock, FakeModule({})))

        self.assertEquals(len(test_suite), len(tests))

        # TODO check order
        for test_number, test in enumerate(test_suite):
            test_call = tests.values()[test_number]
            message = test.messages[0][1]
            self.assertIn(str(test_call), message)
            self.assertIn('Function', message)
            test()

        self.assertEquals(mock.call_args_list, tests.values())

    def test_data_provider_method_messages(self):
        fake_test_case = MockTest()
        fake_module = FakeModule({})

        tests = {'call1': call(1, arg=2), 'call2': call(2, arg=3), 'call3':
            call(3, arg=4)}
        DataProvider(**tests)(fake_test_case.__dict__['test_test'])

        loader = TestLoader()
        test_suite = list(loader.load_object(fake_test_case, fake_module))

        self.assertEquals(len(test_suite), len(tests))

        # TODO check order
        for test_number, test in enumerate(test_suite):
            test_call = tests.values()[test_number]
            message = test.messages[0][1]
            self.assertIn(str(test_call), message)
            self.assertIn('Method', message)
            test()

        self.assertEquals(fake_test_case.set_up_mock.call_count, len(tests))
        self.assertEquals(fake_test_case.test_mock.call_args_list, tests.values())
        self.assertEquals(fake_test_case.tear_down_mock.call_count, len(tests))
