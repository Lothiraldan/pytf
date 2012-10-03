import unittest

try:
    from unittest.mock import Mock, sentinel
except ImportError:
    from mock import Mock, sentinel


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


def MockTest(mock_test_id='test_id'):
    class TestMockClass(object):
        set_up_mock = Mock()
        test_mock = Mock()
        tear_down_mock = Mock()
        test_id = mock_test_id
        init_args = None
        messages = []

        def __init__(self, *args, **kwargs):
            self.init_args = (args, kwargs)

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

# Ressource


def ressource_mock():
    RessourceMock = Mock()
    RessourceMock.set_up.return_value = sentinel.RESSOURCE
    return RessourceMock
