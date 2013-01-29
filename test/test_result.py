import unittest

try:
    from unittest.mock import Mock, call
except ImportError:
    from mock import Mock, call

from pytf.core import TestResult, Test, TestException


class TestResultTestCase(unittest.TestCase):

    def test_simple(self):
        test_id = 'some_test'
        report = TestResult(test_id)

        self.assertEqual(report.id, test_id)
        self.assertEqual(report.success, True)

    def test_failed_test(self):
        with self.assertRaises(TestException) as cm:
            test = Test('test_id', Mock(side_effect=Exception))
            test()

        report = TestResult(test.id, cm.exception)

        self.assertEqual(report.success, False)
        self.assertEqual(report.exception, cm.exception)

    def test_add_message(self):
        test_id = 'some_test'
        report = TestResult(test_id)

        title = 'Title'
        message = 'Message'
        report.add_message(title, message)

        self.assertEqual(list(report.messages), [(title, message)])
