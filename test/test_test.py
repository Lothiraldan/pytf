import unittest

try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

from pytf import Test


class TestTest(unittest.TestCase):

    def test_simple(self):
        def dummy():
            pass

        test = Test(dummy)
        test()

    def test_fail(self):
        class DummyException(Exception):
            pass

        def dummy():
            raise DummyException()

        test = Test(dummy)
        self.assertRaises(DummyException, test)

    def test_setup(self):

        def dummy():
            pass

        setup_mock = Mock()
        test = Test(dummy, setup=setup_mock)
        test()

        self.assertTrue(setup_mock.called)

    def test_teardown(self):

        def dummy():
            pass

        tear_down_mock = Mock()
        test = Test(dummy, tear_down=tear_down_mock)
        test()

        self.assertTrue(tear_down_mock.called)

if __name__ == "__main__":
    unittest.main()
