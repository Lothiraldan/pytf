import unittest

try:
    from unittest.mock import Mock, call
except ImportError:
    from mock import Mock, call

from pytf import TestExecutor
from pytf.core import TestResult

from utils import MockTest


class TestReporterTC(unittest.TestCase):

    def test_one_test(self):
        reporters = [Mock()]
        test_suite = [MockTest()]
        executor = TestExecutor(reporters)
        executor.execute(test_suite)

        expected_calls = [call(TestResult(test_suite[0].test_id))]
        self.assertEquals(reporters[0].show_result.call_args_list,
            expected_calls)

    def test_begin_end(self):
        reporters = [Mock()]
        test_suite = [MockTest()]
        executor = TestExecutor(reporters)
        executor.execute(test_suite)

        self.assertTrue(reporters[0].begin_tests.called)
        self.assertTrue(reporters[0].end_tests.called)


if __name__ == "__main__":
    unittest.main()
