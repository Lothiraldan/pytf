from glob import iglob
from os.path import join

from loaders import TestLoader, UnittestLoader
from core import Test, TestException


class TestRunner(object):

    def __init__(self):
        self.loaders = {}

    def set_loaders(self, loaders):
        self.loaders = loaders

    def _load_modules(self, modules):
        levels = self.loaders.keys()
        levels.sort(reverse=True)

        for module in modules:
            for var_name, var in module.__dict__.items():

                if var_name.startswith('_'):
                    continue

                for loader in self._iter_loaders(levels):
                    test = loader.load_object(var, module)

                    if test:
                        break

    def _iter_loaders(self, levels):
        for level in levels:
            for loader in self.loaders[level]:
                yield loader


class TestFinder(object):

    def __init__(self, path):
        self.path = join(path, '*.py')

    def _find_test_files(self):
        return iglob(self.path)


class TestExecutor(object):

    def __init__(self, test_suite, reporters = ()):
        self.test_suite = test_suite
        self.reporters = reporters

    def execute(self):
        global_test_result = []
        for test in self.test_suite:
            # Prepare test result
            test_result = {'test_id': test.test_id}

            # Run test
            try:
                test()
            except TestException as test_exception:
                test_result['success'] = False
                test_result['exception'] = test_exception
            else:
                test_result['success'] = True

            # Save test result
            global_test_result.append(test_result)

            # TODO: Should be done in a thread??
            for reporter in self.reporters:
                reporter.show_result(test_result)
        return global_test_result
