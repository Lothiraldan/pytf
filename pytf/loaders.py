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
                klass = generator.generate_class(klass)
                for test in self._gen_test_for_class(klass, module):
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
        self.args = args
        self.messages = messages
        self.set_ups = set_ups
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
        test.id += '.' + self.id
        test.messages.extend(self.messages)
        test.set_ups.extend(self.set_ups)
        test.tear_downs.extend(self.tear_downs)
        test.callback = partial(test.callback, *self.args[0], **self.args[1])
        return test

    def generate_class(self, klass):
        klass.id = self.id
        klass.messages = self.messages
        klass.set_ups = self.set_ups
        klass.tear_downs = self.tear_downs
        klass.__init__ = partial_init(klass.__init__, *self.args[0],
            **self.args[1])
        return klass
