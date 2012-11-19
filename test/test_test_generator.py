import unittest

from mock import Mock

from pytf.loaders import TestGenerator


class TestGeneratorTestCase(unittest.TestCase):

    def test_constructor(self):
        # Arguments
        args = ('arg1', 'arg2'), {'arg3': 10, 'arg4': 20}
        generator = TestGenerator(args=args)
        self.assertEqual(generator.args, args)

        # Messages
        messages = [('title', 'message'), ('title2', 'message2')]
        generator = TestGenerator(messages=messages)
        self.assertEqual(generator.messages, messages)

        # Set_up
        set_ups = [Mock(), Mock()]
        generator = TestGenerator(set_ups=set_ups)
        self.assertEqual(generator.set_ups, set_ups)

        # Tear down
        tear_downs = [Mock(), Mock()]
        generator = TestGenerator(tear_downs=tear_downs)
        self.assertEqual(generator.tear_downs, tear_downs)

    def test_merge(self):
        # Generator 1
        generator1_args = ('arg11',), {'arg12': 42}
        generator1_messages = [('title11', 'msg11')]
        generator1_set_ups = [Mock(), Mock()]
        generator1_tear_downs = [Mock(), Mock()]
        generator1 = TestGenerator(args=generator1_args,
            messages=generator1_messages, set_ups=generator1_set_ups,
            tear_downs=generator1_tear_downs)

        # Generator 2
        generator2_args = ('arg21',), {'arg22': 42}
        generator2_messages = [('title21', 'msg21')]
        generator2_set_ups = [Mock(), Mock()]
        generator2_tear_downs = [Mock(), Mock()]
        generator2 = TestGenerator(args=generator2_args,
            messages=generator2_messages, set_ups=generator2_set_ups,
            tear_downs=generator2_tear_downs)

        # Merge generator
        merged_generator = TestGenerator.merge((generator1, generator2))
        merged_args = ['arg11', 'arg21'], {'arg12': 42, 'arg22': 42}
        self.assertEquals(merged_generator.args, merged_args)
        self.assertEquals(merged_generator.messages,
            generator1_messages + generator2_messages)
        self.assertEquals(merged_generator.set_ups,
            generator1_set_ups +  generator2_set_ups)
        self.assertEquals(merged_generator.tear_downs,
            generator1_tear_downs + generator2_tear_downs)