import unittest

from mock import Mock

from pytf.loaders import TestGenerator
from pytf import Test


class TestGeneratorTestCase(unittest.TestCase):

    def test_constructor(self):
        # Base
        test_id = 'test'
        generator = TestGenerator(test_id)
        self.assertEqual(generator.id, test_id)
        self.assertEqual(generator.args, ((), {}))
        self.assertEqual(generator.messages, [])
        self.assertEqual(generator.set_ups, [])
        self.assertEqual(generator.tear_downs, [])

        # Arguments
        args = ('arg1', 'arg2'), {'arg3': 10, 'arg4': 20}
        generator = TestGenerator(test_id, args=args)
        self.assertEqual(generator.args, args)

        # Messages
        messages = [('title', 'message'), ('title2', 'message2')]
        generator = TestGenerator(test_id, messages=messages)
        self.assertEqual(generator.messages, messages)

        # Set_up
        set_ups = [Mock(), Mock()]
        generator = TestGenerator(test_id, set_ups=set_ups)
        self.assertEqual(generator.set_ups, set_ups)

        # Tear down
        tear_downs = [Mock(), Mock()]
        generator = TestGenerator(test_id, tear_downs=tear_downs)
        self.assertEqual(generator.tear_downs, tear_downs)

    def test_merge(self):
        # Generator 1
        generator1_id = 'test_id1'
        generator1_args = ('arg11',), {'arg12': 42}
        generator1_messages = [('title11', 'msg11')]
        generator1_set_ups = [Mock(), Mock()]
        generator1_tear_downs = [Mock(), Mock()]
        generator1 = TestGenerator(generator1_id, args=generator1_args,
            messages=generator1_messages, set_ups=generator1_set_ups,
            tear_downs=generator1_tear_downs)

        # Generator 2
        generator2_id = 'test_id2'
        generator2_args = ('arg21',), {'arg22': 42}
        generator2_messages = [('title21', 'msg21')]
        generator2_set_ups = [Mock(), Mock()]
        generator2_tear_downs = [Mock(), Mock()]
        generator2 = TestGenerator(generator2_id, args=generator2_args,
            messages=generator2_messages, set_ups=generator2_set_ups,
            tear_downs=generator2_tear_downs)

        # Merge generator
        merged_generator = TestGenerator.merge((generator1, generator2))
        merged_args = ['arg11', 'arg21'], {'arg12': 42, 'arg22': 42}
        self.assertEquals(merged_generator.id,
            '.'.join((generator1_id, generator2_id)))
        self.assertEquals(merged_generator.args, merged_args)
        self.assertEquals(merged_generator.messages,
            generator1_messages + generator2_messages)
        self.assertEquals(merged_generator.set_ups,
            generator1_set_ups + generator2_set_ups)
        self.assertEquals(merged_generator.tear_downs,
            generator1_tear_downs + generator2_tear_downs)

    def test_generate_test(self):
        # Generator
        test_id = 'generator'
        generator_args = ('arg11',), {'arg12': 42}
        generator_messages = [('title11', 'msg11')]
        generator_set_ups = [Mock(), Mock()]
        generator_tear_downs = [Mock(), Mock()]
        generator = TestGenerator(test_id, args=generator_args,
            messages=generator_messages, set_ups=generator_set_ups,
            tear_downs=generator_tear_downs)

        # Base test
        test_callback = Mock()
        test = Test('sample', test_callback)

        # Generate it
        generator.generate_test(test)

        # Call it and check it
        test()

        self.assertEqual(test.id, '.'.join(('sample', test_id)))
        self.assertEqual(test_callback.call_args_list[0], generator_args)
        for set_up in generator_set_ups:
            self.assertEqual(set_up.call_count, 1)
        for tear_down in generator_tear_downs:
            self.assertEqual(tear_down.call_count, 1)
        self.assertEqual(test.messages, generator_messages)

    def test_generate_class(self):
        # Generator
        test_id = 'generator'
        generator_args = ('arg11',), {'arg12': 42}
        generator_messages = [('title11', 'msg11')]
        generator_set_ups = [Mock(), Mock()]
        generator_tear_downs = [Mock(), Mock()]
        generator = TestGenerator(test_id, args=generator_args,
            messages=generator_messages, set_ups=generator_set_ups,
            tear_downs=generator_tear_downs)

        # Base test
        class TestClass(object):
            init_mock = Mock()

            def __init__(self, *args, **kwargs):
                self.init_mock(*args, **kwargs)

        # Generate it
        generator.generate_class(TestClass)

        # Call it and check it
        TestClass()

        self.assertEqual(TestClass.id, test_id)
        self.assertEqual(TestClass.init_mock.call_args_list[0], generator_args)
        self.assertEqual(TestClass.set_ups, generator_set_ups)
        self.assertEqual(TestClass.tear_downs, generator_tear_downs)
        self.assertEqual(TestClass.messages, generator_messages)
