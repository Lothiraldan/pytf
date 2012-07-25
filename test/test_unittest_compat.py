import unittest

from pytf import UnittestLoader

from utils import UnittestCaseMock, FakeModule


class UnittestLoaderTestCase(unittest.TestCase):

    def test_unittest_case(self):
        fake_test_case = UnittestCaseMock()

        loader = UnittestLoader()
        fake_module = FakeModule({})
        test_suite = list(loader.load_object(fake_test_case, fake_module))

        self.assertEquals(len(test_suite), 1)
        test_suite[0]()

        self.assertEquals(test_suite[0].test_id,
            '%s.%s.%s' % (fake_module.__name__, fake_test_case.__name__,
            'test_test'))

        self.assertTrue(fake_test_case.set_up_mock.called)
        self.assertTrue(fake_test_case.test_mock.called)
        self.assertTrue(fake_test_case.tear_down_mock.called)

if __name__ == "__main__":
    unittest.main()
