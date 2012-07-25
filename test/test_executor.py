import unittest

try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

from pytf import TestExecutor, Test, TestException

from utils import TestMock


class TestTestExecutor(unittest.TestCase):

    def test_simple(self):
        test_suite = [Mock() for i in xrange(3)]

        test_runner = TestExecutor()
        test_runner.execute(test_suite)

        for test in test_suite:
            self.assertTrue(test.called)

    def test_simple_result(self):
        test_suite = [Test('test_id', Mock())]

        test_runner = TestExecutor()
        test_result = test_runner.execute(test_suite)

        self.assertEqual(len(test_result), 1)
        self.assertEqual(test_result[0]['test_id'], test_suite[0].test_id)
        self.assertEqual(test_result[0]['success'], True)

    def test_simple_fail_result(self):
        test_suite = [Test('test_id', Mock(side_effect=Exception))]

        test_runner = TestExecutor()
        test_result = test_runner.execute(test_suite)

        self.assertEqual(len(test_result), 1)
        self.assertEqual(test_result[0]['test_id'], test_suite[0].test_id)
        self.assertEqual(test_result[0]['success'], False)
        self.assertTrue(isinstance(test_result[0]['exception'], TestException))


if __name__ == "__main__":
    unittest.main()
