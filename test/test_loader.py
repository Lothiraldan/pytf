import unittest

try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

from pytf import TestLoader
from pytf.core import Test
from utils import (FunctionMock, MockTest, MockMultipleTests, FakeModule,
    sample_test_generator)


class DefaultTestLoaderTestCase(unittest.TestCase):

    def test_simple_function(self):
        mock = Mock()
        function_mock = FunctionMock(mock)

        loader = TestLoader()
        fake_module = FakeModule({})
        test_suite = list(loader.load_object(function_mock, fake_module))

        self.assertEquals(len(test_suite), 1)
        test_suite[0]()

        self.assertEquals(test_suite[0].id, '%s.%s' %
            (fake_module.__name__, function_mock.__name__))

        self.assertTrue(mock.called)

    def test_simple_class(self):
        fake_test_case = MockTest()
        fake_module = FakeModule({})

        loader = TestLoader()
        test_suite = list(loader.load_object(fake_test_case, fake_module))

        self.assertEquals(len(test_suite), 1)
        test_suite[0]()

        self.assertEquals(test_suite[0].id, '%s.%s.%s' %
            (fake_module.__name__, fake_test_case.__name__, 'test_test'))

        self.assertTrue(fake_test_case.set_up_mock.called)
        self.assertTrue(fake_test_case.test_mock.called)
        self.assertTrue(fake_test_case.tear_down_mock.called)

    def test_instanciation(self):
        fake_test_case = MockMultipleTests()

        loader = TestLoader()
        test_suite = list(loader.load_object(fake_test_case, FakeModule({})))

        self.assertEquals(len(test_suite), 3)
        for test in test_suite:
            test()

        self.assertEquals(fake_test_case.set_up_mock.call_count, 3)
        self.assertEquals(fake_test_case.test_mock.call_count, 3)
        self.assertEquals(fake_test_case.tear_down_mock.call_count, 3)

        # Check that loader created a new instance for each test in order to
        # avoid edge effect on tests
        self.assertEquals(len(fake_test_case.instances), 3)
        self.assertEquals(len(set(fake_test_case.instances)), 3)


class AdditionnalTestloaderTestCase(unittest.TestCase):

    def test_with_function(self):
        mock = Mock()
        function_mock = FunctionMock(mock)

        sample_loader = Mock()
        test_generator = sample_test_generator()
        sample_loader.load_function.return_value = [test_generator]
        function_mock.loaders = [sample_loader]

        loader = TestLoader()
        test_suite = list(loader.load_object(function_mock, FakeModule({})))

        # Call test
        test_suite[0]()

        # Check loader call
        self.assertEquals(sample_loader.load_function.call_count, 1)
        args = sample_loader.load_function.call_args
        self.assertTrue(isinstance(args[0][0], Test))

        # Check test
        self.assertEqual(mock.call_args, test_generator.args)
        self.assertEqual(test_generator.set_ups[0].call_count, 1)
        self.assertEqual(test_generator.tear_downs[0].call_count, 1)
        self.assertEqual(test_suite[0].messages, test_generator.messages)

    def test_with_class(self):
        fake_test_case = MockTest()
        fake_module = FakeModule({})

        sample_loader = Mock()
        test_generator = sample_test_generator()
        sample_loader.load_class.return_value = [test_generator]
        fake_test_case.loaders = [sample_loader]

        loader = TestLoader()
        test_suite = list(loader.load_object(fake_test_case, fake_module))

        self.assertEquals(len(test_suite), 1)

        self.assertEqual(fake_test_case.init_mock.call_count, 1)
        self.assertEqual(fake_test_case.init_mock.call_args,
            test_generator.args)

    def test_with_test_method(self):
        fake_test_case = MockTest()
        fake_module = FakeModule({})

        sample_loader = Mock()
        test_generator = sample_test_generator()
        sample_loader.load_method.return_value = [test_generator]
        # Simulate method decorator
        fake_test_case.test_test.im_func.loaders = [sample_loader]

        loader = TestLoader()
        test_suite = list(loader.load_object(fake_test_case, fake_module))

        self.assertEquals(len(test_suite), 1)

        # Call test
        test_suite[0]()

        # Check calls
        self.assertEqual(fake_test_case.test_mock.call_count, 1)
        self.assertEqual(fake_test_case.test_mock.call_args,
            test_generator.args)
        self.assertEqual(test_generator.set_ups[0].call_count, 1)
        self.assertEqual(test_generator.tear_downs[0].call_count, 1)
        self.assertEqual(test_suite[0].messages, test_generator.messages)

    def test_with_class_and_test_method(self):
        fake_test_case = MockTest()
        fake_module = FakeModule({})

        sample_loader = Mock()
        sample_loader.load_method.return_value = [sample_test_generator('method_generator')]
        sample_loader.load_class.return_value = [sample_test_generator('class_generator')]

        fake_test_case.loaders = [sample_loader]
        # Simulate method decorator
        fake_test_case.test_test.im_func.loaders = [sample_loader]

        loader = TestLoader()
        test_suite = list(loader.load_object(fake_test_case, fake_module))

        self.assertEquals(len(test_suite), 1)

        test = test_suite[0]
        test()

        # Check id
        self.assertIn('class_generator', test.id)

    def test_with_class_and_test_method_messages(self):
        fake_test_case = MockTest()
        fake_module = FakeModule({})

        sample_loader = Mock()
        sample_loader.load_method.return_value = [sample_test_generator('method_generator')]
        sample_loader.load_class.return_value = [sample_test_generator('class_generator')]

        fake_test_case.loaders = [sample_loader]
        # Simulate method decorator
        fake_test_case.test_test.im_func.loaders = [sample_loader]

        loader = TestLoader()
        test_suite = list(loader.load_object(fake_test_case, fake_module))

        self.assertEquals(len(test_suite), 1)

        messages = sample_test_generator().messages
        self.assertEqual(test_suite[0].messages, messages*2)


if __name__ == "__main__":
    unittest.main()
