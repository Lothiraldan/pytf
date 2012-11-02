import inspect
import unittest

from pytf.core import Test


class TestLoader(object):

    level = 0

    def load_object(self, obj, module):
        if inspect.isfunction(obj):
            return self._load_function(obj, module)

        if inspect.isclass(obj):
            return self._gen_test_for_class(obj, module)

    def _gen_test_for_class(self, klass, module):
        has_set_up = hasattr(klass, 'setUp')
        has_tear_down = hasattr(klass, 'tearDown')

        tests = []
        for test_method_name in filter(lambda x: x.startswith('test'),
                dir(klass)):

            tests.extend(self._load_method(klass, test_method_name, module,
                has_set_up, has_tear_down))

        return tests

    def _load_function(self, function, module):
        if hasattr(function, "loaders"):
            tests = []
            for loader in function.loaders:
                tests.extend(loader.load_function(function, module))
            return tests

        return [Test('%s.%s' % (module.__name__, function.__name__), function)]

    def _load_method(self, klass, method_name, module, has_set_up,
            has_tear_down):
        instance = klass()
        test_method = getattr(instance, method_name)

        if not inspect.ismethod(test_method):
            return []

        if has_set_up:
            set_up_method = getattr(instance, 'setUp', None)

        if has_tear_down:
            tear_down_method = getattr(instance, 'tearDown', None)

        test_id = '%s.%s.%s' % (module.__name__, klass.__name__,
            method_name)
        return [Test(test_id, test_method, set_up=set_up_method,
                tear_down=tear_down_method)]


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
            tests.append(Test(test_id, test_method, set_up=set_up_method,
                    tear_down=tear_down_method))
        return tests
