import inspect

from .loaders import TestLoader
from .loaders import Test

from functools import partial


def DataProvider(fixtures):
    def wrapper(func):
        func.fixtures = fixtures
        return func
    return wrapper


class DataProviderLoader(TestLoader):

    level = 20

    def _load_function(self, function, module):
        if not hasattr(function, 'fixtures'):
            return

        for fixture in function.fixtures:
            yield Test('%s.%s' % (module.__name__, function.__name__),
                partial(function, *fixture[1], **fixture[2]))

    def _load_method(self, klass, method_name, module, has_set_up,
            has_tear_down):
            instance = klass()
            method = getattr(instance, method_name, None)

            if not hasattr(method, 'fixtures'):
                return []

            if not inspect.ismethod(method):
                return []

            tests = []
            for fixture in method.fixtures:
                instance = klass()

                if has_set_up:
                    set_up_method = getattr(instance, 'setUp', None)

                if has_tear_down:
                    tear_down_method = getattr(instance, 'tearDown', None)

                test_id = '%s.%s.%s' % (module.__name__, klass.__name__,
                    method_name)
                tests.append(Test(test_id,
                        partial(method, *fixture[1], **fixture[2]),
                        set_up=set_up_method, tear_down=tear_down_method))
            return tests
