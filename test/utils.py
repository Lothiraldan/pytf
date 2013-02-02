import unittest

try:
    from unittest.mock import Mock, sentinel
except ImportError:
    from mock import Mock, sentinel

from pytf.loaders import TestGenerator


class FakeModule(object):

    def __init__(self, module_dict):
        self.__dict__ = module_dict
        self.__name__ = 'fake_module'


class LoaderMock(Mock):
    level = 0


def FunctionMock(Mock):
    def call(*args, **kwargs):
        return call.mock(*args, **kwargs)
    call.mock = Mock
    return call


def MockTest():
    class TestMockClass(object):
        set_up_mock = Mock()
        test_mock = Mock()
        tear_down_mock = Mock()
        init_mock = Mock()
        messages = []

        def __init__(self, *args, **kwargs):
            self.init_mock(*args, **kwargs)

        def setUp(self):
            self.set_up_mock()

        def test_test(self, *args, **kwargs):
            self.test_mock(*args, **kwargs)

        def tearDown(self):
            self.tear_down_mock()
    return TestMockClass


def MockMultipleTests():
    class TestMockClass(object):

        instances = []

        set_up_mock = Mock()
        test_mock = Mock()
        tear_down_mock = Mock()

        def setUp(self):
            TestMockClass.instances.append(self)
            self.set_up_mock()

        def test_test_1(self):
            self.test_mock()

        def test_test_2(self):
            self.test_mock()

        def test_test_3(self):
            self.test_mock()

        def tearDown(self):
            self.tear_down_mock()
    return TestMockClass


def UnittestCaseMock():
    class UnittestCaseMockClass(unittest.TestCase):
        set_up_mock = Mock()
        test_mock = Mock()
        tear_down_mock = Mock()

        def setUp(self):
            self.set_up_mock()

        def test_test(self):
            self.test_mock()
            self.assertTrue(True)
            self.assertFalse(False)
            self.assertEqual(0, 0)
            self.assertRaises(IndexError, lambda: [][1])

        def tearDown(self):
            self.tear_down_mock()
    return UnittestCaseMockClass

def sample_test_generator():
    generator_args = ('arg11',), {'arg12': 42}
    generator_messages = [('title11', 'msg11')]
    generator_set_ups = [Mock()]
    generator_tear_downs = [Mock()]
    return TestGenerator('sample_test_generator', args=generator_args,
        messages=generator_messages, set_ups=generator_set_ups,
        tear_downs=generator_tear_downs)

# Ressource

def ressource_mock():
    RessourceMock = Mock()
    RessourceMock.set_up.return_value = {'ressource': sentinel.RESSOURCE}
    return RessourceMock
