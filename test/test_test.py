import unittest
import inspect

try:
    from unittest.mock import Mock, call
except ImportError:
    from mock import Mock, call

from pytf import Test, TestException

import traceback


class TestTest(unittest.TestCase):

    def test_simple(self):
        dummy = Mock()

        test = Test('id', dummy)
        test()

        self.assertTrue(dummy.called)

    def test_setup(self):
        setup_mock = Mock()
        test = Test('id', Mock(), set_ups=setup_mock)
        test()

        self.assertTrue(setup_mock.called)

    def test_setup_pass_the_result(self):
        result = {'arg1': 'val1', 'arg2': 'val2'}

        setup_mock = Mock()
        setup_mock.pass_return_value = True
        setup_mock.return_value = result
        callback = Mock()
        test = Test('id', callback, set_ups=setup_mock)

        test()

        self.assertEqual(callback.call_args_list, [call(**result)])

    def test_multiple_setup(self):
        setup_mocks = [Mock(), Mock(), Mock()]
        test = Test('id', Mock(), set_ups=setup_mocks)
        test()

        for mock in setup_mocks:
            self.assertTrue(mock.called)

    def test_teardown(self):
        tear_down_mock = Mock()
        test = Test('id', Mock(), tear_downs=tear_down_mock)
        test()

        self.assertTrue(tear_down_mock.called)

    def test_multiple_teardown(self):
        teardown_mocks = [Mock(), Mock(), Mock()]
        test = Test('id', Mock(), tear_downs=teardown_mocks)
        test()

        for mock in teardown_mocks:
            self.assertTrue(mock.called)

    def test_message(self):
        msg_title = 'Message'
        msg_content = 'Content'

        test = Test('id', Mock())
        test.add_message(msg_title, msg_content)
        self.assertEqual([(msg_title, msg_content)], list(test.messages))


class TestTestException(unittest.TestCase):

    def test_during_main_test(self):
        exception_class = KeyError
        fail_test = Mock(side_effect=exception_class)

        test_id = 'failing_test'
        test = Test(test_id, fail_test)

        with self.assertRaises(TestException) as exc:
            test()

        exc = exc.exception
        self.assertEqual(exc.test_id, test_id)
        self.assertEqual(exc.phase, 'test')
        self.assertEqual(exc.callable, fail_test)
        self.assertEqual(exc.exc_info[0], exception_class)
        self.assertTrue(inspect.istraceback(exc.exc_info[2]))

    def test_during_set_up(self):
        exception_class = KeyError
        fail_set_up = Mock(side_effect=exception_class)

        test_id = 'failing_set_up'
        test = Test(test_id, Mock(), set_ups=fail_set_up)

        with self.assertRaises(TestException) as exc:
            test()

        exc = exc.exception
        self.assertEqual(exc.test_id, test_id)
        self.assertEqual(exc.phase, 'set_up')
        self.assertEqual(exc.callable, fail_set_up)
        self.assertEqual(exc.exc_info[0], exception_class)
        self.assertTrue(inspect.istraceback(exc.exc_info[2]))

    def test_during_tear_down(self):
        exception_class = KeyError
        fail_tear_down = Mock(side_effect=exception_class)

        test_id = 'failing_tear_down'
        test = Test(test_id, Mock(), tear_downs=fail_tear_down)

        with self.assertRaises(TestException) as exc:
            test()

        exc = exc.exception
        self.assertEqual(exc.test_id, test_id)
        self.assertEqual(exc.phase, 'tear_down')
        self.assertEqual(exc.callable, fail_tear_down)
        self.assertEqual(exc.exc_info[0], exception_class)
        self.assertTrue(inspect.istraceback(exc.exc_info[2]))

if __name__ == "__main__":
    unittest.main()
