import unittest

from pytf import UnittestLoader

from utils import UnittestCaseMock, FakeModule


class UnittestLoaderTestCase(unittest.TestCase):

    def test_unittest_case(self):
        fake_test_case = UnittestCaseMock()

        loader = UnittestLoader()
        test_suite = list(loader.load_object(fake_test_case, FakeModule({})))

        self.assertEquals(len(test_suite), 1)
        test_suite[0]()

        self.assertTrue(fake_test_case.set_up_mock.called)
        self.assertTrue(fake_test_case.test_mock.called)
        self.assertTrue(fake_test_case.tear_down_mock.called)

if __name__ == "__main__":
    unittest.main()
