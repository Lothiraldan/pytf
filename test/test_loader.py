import unittest

try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

from pytf import TestLoader
from utils import FunctionMock, TestMock, TestMockMultipleTests, FakeModule


class TestLoaderTestCase(unittest.TestCase):

    def test_simple_function(self):
        mock_function = Mock()

        loader = TestLoader()
        test_suite = list(loader.load_object(FunctionMock(mock_function),
            FakeModule({})))

        self.assertEquals(len(test_suite), 1)
        test_suite[0]()

        self.assertTrue(mock_function.called)

    def test_simple_class(self):
        fake_test_case = TestMock()

        loader = TestLoader()
        test_suite = list(loader.load_object(fake_test_case, FakeModule({})))

        self.assertEquals(len(test_suite), 1)
        test_suite[0]()

        self.assertTrue(fake_test_case.set_up_mock.called)
        self.assertTrue(fake_test_case.test_mock.called)
        self.assertTrue(fake_test_case.tear_down_mock.called)

    def test_instanciation(self):
        fake_test_case = TestMockMultipleTests()

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

if __name__ == "__main__":
    unittest.main()
