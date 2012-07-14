import unittest

try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

from pytf import TestExecutor


class TestTestExecutor(unittest.TestCase):

    def test_simple(self):
        test_suite = [Mock() for i in xrange(3)]

        test_runner = TestExecutor(test_suite)
        test_runner.execute()

        for test in test_suite:
            self.assertTrue(test.called)

if __name__ == "__main__":
    unittest.main()
