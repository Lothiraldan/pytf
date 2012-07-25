import inspect
import unittest

from pytf.core import Test


class TestLoader(object):

    level = 0

    def load_object(self, obj, module):
        if inspect.isfunction(obj):
            return [Test('%s.%s' % (module.__name__, obj.__name__), obj)]

        if inspect.isclass(obj):
            return self._gen_test_for_class(obj, module)

    def _gen_test_for_class(self, klass, module):
        has_set_up = False
        if hasattr(klass, 'setUp'):
            has_set_up = True

        has_tear_down = False
        if hasattr(klass, 'tearDown'):
            has_tear_down = True

        tests = []
        for test_method_name in filter(lambda x: x.startswith('test'), dir(klass)):

            instance = klass()

            test_method = getattr(instance, test_method_name)
            if not inspect.ismethod(test_method):
                continue

            set_up_method = None
            if has_set_up:
                set_up_method = getattr(instance, 'setUp')

            tear_down_method = None
            if has_tear_down:
                tear_down_method = getattr(instance, 'tearDown')

            test_id = '%s.%s.%s' % (module.__name__, klass.__name__,
                test_method_name)
            tests.append(Test(test_id, test_method, set_up=set_up_method,
                    tear_down=tear_down_method))
        return tests


# Unittest compatibility loader
class UnittestLoader(TestLoader):

    level = 10

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
