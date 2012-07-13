from mock import Mock


class FakeModule(object):

    def __init__(self, module_dict):
        self.__dict__ = module_dict


def FunctionMock(Mock):
    def call(mock=Mock):
        mock()
    return call


def TestMock():
    class TestMockClass(object):
        set_up_mock = Mock()
        test_mock = Mock()
        tear_down_mock = Mock()

        def setUp(self):
            self.set_up_mock()

        def test_test(self):
            self.test_mock()

        def tearDown(self):
            self.tear_down_mock()
    return TestMockClass
