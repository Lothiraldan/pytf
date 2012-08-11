import os
import inspect

from glob import iglob
from contextlib import nested
from os.path import join, relpath, splitext
from importlib import import_module
from collections import defaultdict
from operator import methodcaller


from pytf.loaders import TestLoader, UnittestLoader
from pytf.core import Test, TestException, TestResult
from pytf.reporters import TextTestReporter
from pytf.contexts import StdCatcher

__all__ = ['TestLoader', 'UnittestLoader', 'Test', 'TextTestReporter']


class TestFinder(object):

    def __init__(self, path, pattern=None):
        if pattern is None:
            pattern = 'test*.py'
        self.path = join(path, pattern)

    def find(self):
        for path in iglob(self.path):
            if path.endswith('__init__.py'):
                continue
            else:
                yield path


class TestExecutor(object):

    def __init__(self, reporters=(), contexts=()):
        self.reporters = reporters
        self.contexts = contexts

    def execute(self, test_suite):
        global_test_result = []
        # Start reporters
        map(methodcaller('begin_tests'), self.reporters)
        # Run tests
        for test in test_suite:
            # Call contexts
            map(methodcaller('enter'), self.contexts)

            # Run test
            try:
                test()
            except TestException as test_exception:
                test_result = TestResult(test.test_id, test_exception)
            else:
                test_result = TestResult(test.test_id)

            # Call contexts end
            for context in self.contexts:
                context.exit(test_result)

            # Save test result
            global_test_result.append(test_result)

            # TODO: Should be done in a thread??
            for reporter in self.reporters:
                reporter.show_result(test_result)
        # Stop reporters
        map(methodcaller('end_tests'), self.reporters)
        return global_test_result


class TestRunner(object):

    def __init__(self, finders, loaders=None, executor=None):
        self.finders = finders
        if executor is None:
            executor = TestExecutor([TextTestReporter()],
                contexts=[StdCatcher()])
        self.executor = executor

        self.loaders = defaultdict(list)
        if loaders is None:
            loaders = (TestLoader(),)
        self.set_loaders(loaders)

    def set_loaders(self, loaders):
        for loader in loaders:
            self.loaders[loader.level].append(loader)

    def _load_modules(self, modules):
        levels = self.loaders.keys()
        levels.sort(reverse=True)

        all_tests = []

        for module in modules:
            for var_name, var in module.__dict__.items():

                if var_name.startswith('_'):
                    continue

                if not (var_name.startswith('test') or
                    var_name.startswith('Test')) and not inspect.isclass(var):
                    continue

                for loader in self._iter_loaders(levels):
                    tests = loader.load_object(var, module)

                    if tests:
                        all_tests.extend(tests)
                        break

        return all_tests

    def _iter_loaders(self, levels):
        for level in levels:
            for loader in self.loaders[level]:
                yield loader

    def run(self):
        test_suite = self._build_test_suite()
        self.executor.execute(test_suite)

    def _build_test_suite(self):
        modules = []

        for finder in self.finders:
            for path in finder.find():
                modules.append(self._get_module(path))
        return self._load_modules(modules)

    def _get_module(self, path):
        ''' Try to import it, else read it and compile it. TODO implement it
        correctly
        '''
        modname = relpath(path)
        splitted_modname = splitext(modname)[0].split(os.sep)
        modname = '.'.join(splitted_modname)

        module = import_module(modname)

        return module
