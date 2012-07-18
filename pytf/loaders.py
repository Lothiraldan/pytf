import inspect
import unittest

from pytf.core import Test


class TestLoader(object):

    def load_object(self, obj, module):
        if inspect.isfunction(obj):
            yield Test('id', obj)

        if inspect.isclass(obj):
            for test in self._gen_test_for_class(obj):
                yield test

    def _gen_test_for_class(self, klass):
        has_set_up = False
        if hasattr(klass, 'setUp'):
            has_set_up = True

        has_tear_down = False
        if hasattr(klass, 'tearDown'):
            has_tear_down = True

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

            test_id = 'test'
            yield Test(test_id, test_method, set_up=set_up_method,
                    tear_down=tear_down_method)


# Unittest compatibility loader
class UnittestLoader(TestLoader):
    def load_object(self, klass, module):
        if not issubclass(klass, unittest.TestCase):
            return

        for test_method_name in filter(lambda x: x.startswith('test'), dir(klass)):

            instance = klass(test_method_name)

            test_method = getattr(instance, test_method_name)
            if not inspect.ismethod(test_method):
                continue

            set_up_method = getattr(instance, 'setUp')

            tear_down_method = getattr(instance, 'tearDown')

            test_id = "%s.%s" % (module.__name__, klass.__name__)
            yield Test(test_id, test_method, set_up=set_up_method,
                    tear_down=tear_down_method)
