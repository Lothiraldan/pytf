from time import sleep


class TestCase(object):

    def test_fail(self):
        1/0

    def test_dependency(self):
        self.test_fail()
