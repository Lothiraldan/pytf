import unittest

try:
    from unittest.mock import Mock, call
except ImportError:
    from mock import Mock, call

from tempfile import mkdtemp
from os.path import join

from pytf import TestLoader
from pytf.dataprovider import DataProviderLoader, DataProvider
from pytf.scenario import ScenarioTestCase, ScenarioLoader
from pytf.ressources import RessourcesLoader, Ressources
from utils import (FunctionMock, MockTest, MockMultipleTests, FakeModule,
    ressource_mock)


class TestLoaderTestCase(unittest.TestCase):

    def test_simple_function(self):
        mock = Mock()
        function_mock = FunctionMock(mock)

        loader = TestLoader()
        fake_module = FakeModule({})
        test_suite = list(loader.load_object(function_mock, fake_module))

        self.assertEquals(len(test_suite), 1)
        test_suite[0]()

        self.assertEquals(test_suite[0].test_id, '%s.%s' %
            (fake_module.__name__, function_mock.__name__))

        self.assertTrue(mock.called)

    def test_simple_class(self):
        fake_test_case = MockTest()
        fake_module = FakeModule({})

        loader = TestLoader()
        test_suite = list(loader.load_object(fake_test_case, fake_module))

        self.assertEquals(len(test_suite), 1)
        test_suite[0]()

        self.assertEquals(test_suite[0].test_id, '%s.%s.%s' %
            (fake_module.__name__, fake_test_case.__name__, 'test_test'))

        self.assertTrue(fake_test_case.set_up_mock.called)
        self.assertTrue(fake_test_case.test_mock.called)
        self.assertTrue(fake_test_case.tear_down_mock.called)

    def test_instanciation(self):
        fake_test_case = MockMultipleTests()

        loader = TestLoader()
        test_suite = list(loader.load_object(fake_test_case, FakeModule({})))

        self.assertEquals(len(test_suite), 3)
        for test in test_suite:
            test()

        self.assertEquals(fake_test_case.set_up_mock.call_count, 3)
        self.assertEquals(fake_test_case.test_mock.call_count, 3)
        self.assertEquals(fake_test_case.tear_down_mock.call_count, 3)

        # Check that loader created a new instance for each test in order to
        # avoid edge effect on tests
        self.assertEquals(len(fake_test_case.instances), 3)
        self.assertEquals(len(set(fake_test_case.instances)), 3)


class DataProviderLoaderTestCase(unittest.TestCase):

    def test_data_provider_function(self):
        mock = Mock()
        function_mock = FunctionMock(mock)

        tests = [call(1, arg=2), call(2, arg=3), call(3, arg=4)]
        DataProvider(tests)(function_mock)

        loader = DataProviderLoader()
        test_suite = list(loader.load_object(function_mock, FakeModule({})))

        self.assertEquals(len(test_suite), len(tests))

        for test in test_suite:
            test()

        self.assertEquals(mock.call_args_list, tests)

    def test_data_provider_method(self):
        fake_test_case = MockTest()
        fake_module = FakeModule({})

        tests = [call(1, arg=2), call(2, arg=3), call(3, arg=4)]
        DataProvider(tests)(fake_test_case.__dict__['test_test'])

        loader = DataProviderLoader()
        test_suite = list(loader.load_object(fake_test_case, fake_module))

        self.assertEquals(len(test_suite), len(tests))

        for test in test_suite:
            test()

        self.assertEquals(fake_test_case.set_up_mock.call_count, len(tests))
        self.assertEquals(fake_test_case.test_mock.call_args_list, tests)
        self.assertEquals(fake_test_case.tear_down_mock.call_count, len(tests))

    def test_data_provider_class(self):
        fake_test_case = MockTest()
        fake_module = FakeModule({})

        tests = [call(1, arg=2), call(2, arg=3), call(3, arg=4)]
        DataProvider(tests)(fake_test_case)

        loader = DataProviderLoader()
        test_suite = list(loader.load_object(fake_test_case, fake_module))

        self.assertEquals(len(test_suite), len(tests))

        for test in test_suite:
            test()

    def test_data_provider_class_and_method(self):
        fake_test_case = MockTest()
        fake_module = FakeModule({})

        class_tests = [call(1, arg=2), call(2, arg=3), call(3, arg=4)]
        DataProvider(class_tests)(fake_test_case)

        method_tests = [call(4, arg=5), call(5, arg=6), call(6, arg=7)]
        DataProvider(method_tests)(fake_test_case.__dict__['test_test'])

        loader = DataProviderLoader()
        test_suite = list(loader.load_object(fake_test_case, fake_module))

        self.assertEquals(len(test_suite), len(class_tests) * len(method_tests))

        for test in test_suite:
            test()

    def test_data_provider_function_messages(self):
        mock = Mock()
        function_mock = FunctionMock(mock)

        tests = [call(1, arg=2), call(2, arg=3), call(3, arg=4)]
        DataProvider(tests)(function_mock)

        loader = DataProviderLoader()
        test_suite = list(loader.load_object(function_mock, FakeModule({})))

        self.assertEquals(len(test_suite), len(tests))

        for test_number, test in enumerate(test_suite):
            test_call = tests[test_number]
            self.assertEquals(test.messages, [('DataProvider',
                (test_call[1], test_call[2]))])
            test()

        self.assertEquals(mock.call_args_list, tests)

    def test_data_provider_method_messages(self):
        fake_test_case = MockTest()
        fake_module = FakeModule({})

        tests = [call(1, arg=2), call(2, arg=3), call(3, arg=4)]
        DataProvider(tests)(fake_test_case.__dict__['test_test'])

        loader = DataProviderLoader()
        test_suite = list(loader.load_object(fake_test_case, fake_module))

        self.assertEquals(len(test_suite), len(tests))

        for test_number, test in enumerate(test_suite):
            test_call = tests[test_number]
            self.assertEquals(test.messages, [('DataProvider',
                (test_call[1], test_call[2]))])
            test()

        self.assertEquals(fake_test_case.set_up_mock.call_count, len(tests))
        self.assertEquals(fake_test_case.test_mock.call_args_list, tests)
        self.assertEquals(fake_test_case.tear_down_mock.call_count, len(tests))


class RessourceLoaderTestCase(unittest.TestCase):

    def test_ressource_function(self):
        mock = Mock()
        function_mock = FunctionMock(mock)

        ressource = ressource_mock()
        Ressources([ressource])(function_mock)

        loader = RessourcesLoader()
        test_suite = list(loader.load_object(function_mock, FakeModule({})))

        self.assertEquals(len(test_suite), 1)

        for test in test_suite:
            test()

        self.assertEquals(ressource.set_up.call_args_list, [call()])
        self.assertEquals(mock.call_args_list,
            [call(**ressource.set_up.return_value)])
        self.assertEquals(ressource.tear_down.call_args_list, [call()])


# class TestScenarioTestCase(unittest.TestCase):

#     def setUp(self):

#         class ScenarioTest(ScenarioTestCase):
#             scenario_directory = mkdtemp()

#             def test_scenario(self):
#                 self.test_scenario()

#         self.test_case = ScenarioTest()
#         self.fake_module = FakeModule({})

#         self.loader = ScenarioLoader()

#     def test_one_scenario_file(self):

#         with open(join(self.scenario_directory, 'test1.py'), 'w') as f:
#             f.write('')

#         test_suite = list(self.loader.load_object(self.test_case,
#             self.fake_module))

#         self.assertEquals(len(test_suite), 1)

#         for test in test_suite:
#             test()


if __name__ == "__main__":
    unittest.main()
