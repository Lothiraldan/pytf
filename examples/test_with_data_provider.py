from pytf.dataprovider import DataProvider, call


@DataProvider(max_5=call(max=5), max_10=call(max=10), max_15=call(max=15))
class TestCase(object):
    def __init__(self, max):
        self.max = max

    @DataProvider(n_3=call(n=3), n_7=call(n=7), n_12=call(n=12), n_20=call(n=20))
    def test_test(self, n):
        assert n < self.max
