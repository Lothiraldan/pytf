import inspect

from glob import iglob
from os.path import join


class Test(object):

    def __init__(self, callback, setup=None, tear_down=None):
        self.callback = callback
        self.setup = setup
        self.tear_down = tear_down

    def __call__(self):
        if self.setup:
            self.setup()
        self.callback()
        if self.tear_down:
            self.tear_down()


class TestLoader(object):

    def load_module(self, module):
        for var in module.__dict__.values():
            if inspect.isfunction(var):
                yield Test(var)

            if inspect.isclass(var):
                instance = var()

                set_up_method = None
                if hasattr(instance, 'setUp'):
                    set_up_method = instance.setUp

                tear_down_method = None
                if hasattr(instance, 'tearDown'):
                    tear_down_method = instance.tearDown

                for instance_var_name in dir(instance):
                    if not instance_var_name.startswith('test'):
                        continue

                    instance_var = getattr(instance, instance_var_name)
                    if not inspect.ismethod(instance_var):
                        continue

                    yield Test(instance_var, setup=set_up_method,
                            tear_down=tear_down_method)


class TestFinder(object):

    def __init__(self, path):
        self.path = join(path, '*.py')

    def _find_test_files(self):
        return iglob(self.path)


class TestRunner(object):

    def __init__(self, test_suite):
        self.test_suite = test_suite

    def run(self):
        for test in self.test_suite:
            test()
