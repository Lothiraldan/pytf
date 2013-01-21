import inspect

from .loaders import TestLoader, Test

from functools import partial


def DataProvider(fixtures):
    def wrapper(func):
        func.fixtures = fixtures
        return func
    return wrapper


class DataProviderLoader(TestLoader):

    level = 10

    def _load_function(self, function, module):
        if not hasattr(function, 'fixtures'):
            return

        for fixture in function.fixtures:
            test = Test('%s.%s' % (module.__name__, function.__name__),
                partial(function, *fixture[1], **fixture[2]))
            test.add_message('DataProvider', (fixture[1], fixture[2]))
            yield test

    def _load_method(self, klass, method_name, module, has_set_up,
        has_tear_down):

        method = getattr(klass, method_name)
        method_fixtures = getattr(method, 'fixtures', (None,))

        if not inspect.ismethod(method):
            return []

        tests = []

        for instance in self._gen_instances(klass):

            for fixture in method_fixtures:

                method = getattr(instance, method_name)

                set_up_method = getattr(instance, 'setUp', None)
                tear_down_method = getattr(instance, 'tearDown', None)

                test_id = '%s.%s.%s' % (module.__name__, klass.__name__,
                    method_name)
                if fixture is None:
                    tests.append(Test(test_id, method))
                else:
                    test = Test(test_id,
                        partial(method, *fixture[1], **fixture[2]),
                        set_ups=set_up_method, tear_downs=tear_down_method)
                    test.add_message('DataProvider',
                        (fixture[1], fixture[2]))
                    tests.append(test)
        return tests

    def _gen_instances(self, klass):
        if hasattr(klass, 'fixtures'):
            for fixture in klass.fixtures:
                yield klass(*fixture[1], **fixture[2])
        else:
            yield klass()
