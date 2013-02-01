import inspect
import unittest

from itertools import product
from functools import partial

from pytf.core import Test


class TestLoader(object):

    level = 0

    def load_object(self, obj, module):
        if inspect.isfunction(obj):
            return self._load_function(obj, module)

        if inspect.isclass(obj):
            return self._load_class(obj, module)

    def _load_function(self, function, module):
        test = Test('%s.%s' % (module.__name__, function.__name__), function)

        if hasattr(function, "loaders"):
            generators = [loader.load_function(test) for loader in
                function.loaders]
            for combination in product(*generators):
                generator = TestGenerator.merge(combination)
                yield generator.generate_test(test)
        else:
            yield test

    def _load_class(self, klass, module):
        if hasattr(klass, 'loaders'):
            generators = [loader.load_class(klass) for loader in
                klass.loaders]
            for combination in product(*generators):
                generator = TestGenerator.merge(combination)
                generated_klass = generator.generate_class(klass)
                for test in self._gen_test_for_class(generated_klass, module):
                    yield test
        else:
            for test in self._gen_test_for_class(klass, module):
                yield test

    def _gen_test_for_class(self, klass, module):
        for test_method_name in filter(lambda x: x.startswith('test'),
                dir(klass)):

            if not inspect.ismethod(getattr(klass, test_method_name)):
                continue

            for test in self._load_method(klass, test_method_name, module):
                yield test

    def _load_method(self, klass, method_name, module):
        instance = klass()
        test_method = getattr(instance, method_name)

        set_up_method = getattr(instance, 'setUp', None)
        tear_down_method = getattr(instance, 'tearDown', None)

        test_id = '%s.%s.%s' % (module.__name__, klass.__name__,
            method_name)
        test = Test(test_id, test_method, set_ups=set_up_method,
                tear_downs=tear_down_method)

        if hasattr(test_method, 'loaders'):
            generators = [loader.load_method(test) for loader in
                test_method.loaders]
            for combination in product(*generators):
                generator = TestGenerator.merge(combination)
                yield generator.generate_test(test)
        else:
            yield test


# Unittest compatibility loader
class UnittestLoader(TestLoader):

    level = 20

    def load_object(self, klass, module):
        if not inspect.isclass(klass):
            return

        if not issubclass(klass, unittest.TestCase):
            return

        tests = []
        for test_method_name in filter(lambda x: x.startswith('test'), dir(klass)):

            instance = klass(test_method_name)

            test_method = getattr(instance, test_method_name)
            if not inspect.ismethod(test_method):
                continue

            set_up_method = getattr(instance, 'setUp')

            tear_down_method = getattr(instance, 'tearDown')

            test_id = "%s.%s.%s" % (module.__name__, klass.__name__,
                test_method_name)
            tests.append(Test(test_id, test_method, set_ups=set_up_method,
                    tear_downs=tear_down_method))
        return tests


def partial_init(f, *args, **kwargs):
    def wrapped(self, *fargs, **fkwargs):
        newkwargs = kwargs.copy()
        newkwargs.update(fkwargs)
        return f(self, *(args + fargs), **newkwargs)
    return wrapped


class TestGenerator(object):

    def __init__(self, test_id, args=None, messages=None, set_ups=None,
                 tear_downs=None):
        self.id = test_id

        if args is None:
            args = ((), {})
        self.args = args

        if messages is None:
            messages = []
        self.messages = messages

        if set_ups is None:
            set_ups = []
        self.set_ups = set_ups

        if tear_downs is None:
            tear_downs = []
        self.tear_downs = tear_downs

    @staticmethod
    def merge(generators):
        test_ids = []
        args = ([], {})
        messages = []
        set_ups = []
        tear_downs = []

        for generator in generators:
            test_ids.append(generator.id)
            args[0].extend(generator.args[0])
            args[1].update(generator.args[1])
            messages.extend(generator.messages)
            set_ups.extend(generator.set_ups)
            tear_downs.extend(generator.tear_downs)

        return TestGenerator('.'.join(test_ids), args, messages, set_ups,
            tear_downs)

    def generate_test(self, test):
        test_id = test.id + '.' + self.id
        test_messages = test.messages + self.messages
        test_set_ups = test.set_ups + self.set_ups
        test_tear_downs = test.tear_downs + self.tear_downs
        test_callback = partial(test.callback, *self.args[0], **self.args[1])

        generated_test = Test(test_id, test_callback, test_set_ups,
            test_tear_downs)
        for message_title, message_content in test_messages:
            generated_test.add_message(message_title, message_content)
        return generated_test

    def generate_class(self, klass):
        # Generate a copy of initial klass with same name
        generated_klass = type(klass.__name__, klass.__bases__,
            dict(klass.__dict__))
        generated_klass.id = self.id
        generated_klass.messages = self.messages
        generated_klass.set_ups = self.set_ups
        generated_klass.tear_downs = self.tear_downs
        generated_klass.__init__ = partial_init(generated_klass.__init__,
            *self.args[0], **self.args[1])
        return generated_klass
