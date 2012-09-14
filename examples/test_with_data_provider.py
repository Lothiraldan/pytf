from pytf.dataprovider import DataProvider

try:
    from unittest.mock import call
except ImportError:
    from mock import call


@DataProvider([call(max=5), call(max=10), call(max=15)])
class TestCase(object):
    def __init__(self, max):
        self.max = max

    @DataProvider([call(n=3), call(n=7), call(n=12), call(n=20)])
    def test_test(self, n):
        assert n < self.max
