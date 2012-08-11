import unittest

try:
    from unittest.mock import Mock, call
except ImportError:
    from mock import Mock, call

from pytf import TestExecutor, Test, TestException


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
        self.assertEqual(test_result[0].test_id, test_suite[0].test_id)
        self.assertEqual(test_result[0].success, True)

    def test_simple_fail_result(self):
        test_suite = [Test('test_id', Mock(side_effect=Exception))]

        test_runner = TestExecutor()
        test_result = test_runner.execute(test_suite)

        self.assertEqual(len(test_result), 1)
        self.assertEqual(test_result[0].test_id, test_suite[0].test_id)
        self.assertEqual(test_result[0].success, False)
        self.assertTrue(isinstance(test_result[0].exception, TestException))

    def test_contexts(self):
        test_suite = [Test('test_id', Mock())]

        context_mock = Mock()
        context_mock.exit.return_value = None
        test_runner = TestExecutor(contexts=[context_mock])
        test_result = test_runner.execute(test_suite)

        self.assertTrue(context_mock.enter.called)
        self.assertEqual(context_mock.exit.call_args_list,
            [call(test_result[0])])

    def test_contexts_add_message(self):
        test_suite = [Test('test_id', Mock())]

        context_mock = Mock()
        title = 'Title'
        message = 'Message'
        context_mock.exit.side_effect = lambda result: \
            result.add_message(title, message)

        test_runner = TestExecutor(contexts=[context_mock])
        test_result = test_runner.execute(test_suite)

        self.assertEqual(test_result[0].test_id, test_suite[0].test_id)
        self.assertEqual(test_result[0].success, True)
        self.assertEqual(test_result[0].messages, [{'title': title,
            'message': message}])


if __name__ == "__main__":
    unittest.main()
