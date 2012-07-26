import unittest

try:
    from unittest.mock import Mock, call
except ImportError:
    from mock import Mock, call

from pytf import TestExecutor

from utils import MockTest

class TestReporterTC(unittest.TestCase):

    def test_one_test(self):
        reporters = [Mock()]
        test_suite = [MockTest()]
        executor = TestExecutor(reporters)
        executor.execute(test_suite)

        report = {'test_id': test_suite[0].test_id, 'success': True}
        expected_calls = [call(report)]
        self.assertEquals(reporters[0].show_result.call_args_list,
            expected_calls)


if __name__ == "__main__":
    unittest.main()
