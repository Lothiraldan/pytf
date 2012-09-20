import unittest
import inspect

try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

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
        test = Test('id', Mock(), set_up=setup_mock)
        test()

        self.assertTrue(setup_mock.called)

    def test_teardown(self):
        tear_down_mock = Mock()
        test = Test('id', Mock(), tear_down=tear_down_mock)
        test()

        self.assertTrue(tear_down_mock.called)

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
        test = Test(test_id, Mock(), set_up=fail_set_up)

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
        test = Test(test_id, Mock(), tear_down=fail_tear_down)

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
