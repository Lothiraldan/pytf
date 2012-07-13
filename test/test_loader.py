import unittest

from mock import Mock

from pytf import TestLoader
from utils import FunctionMock, FakeModule, TestMock


class TestLoaderTestCase(unittest.TestCase):

    def test_simple_function(self):
        mock_function = Mock()

        module = FakeModule({'simple_test': FunctionMock(mock_function)})

        loader = TestLoader()
        test_suite = list(loader.load_module(module))

        self.assertEquals(len(test_suite), 1)
        test_suite[0]()

        self.assertTrue(mock_function.called)

    def test_simple_class(self):
        fake_test_case = TestMock()

        module = FakeModule({'simple_test': fake_test_case})

        loader = TestLoader()
        test_suite = list(loader.load_module(module))

        self.assertEquals(len(test_suite), 1)
        test_suite[0]()

        self.assertTrue(fake_test_case.set_up_mock.called)
        self.assertTrue(fake_test_case.test_mock.called)
        self.assertTrue(fake_test_case.tear_down_mock.called)

if __name__ == "__main__":
    unittest.main()
