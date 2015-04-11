# -*- coding: utf-8 -*-

__author__ = 'Boris Feld'
__email__ = 'lothiraldan@gmail.com'
__version__ = '0.1.0'

import os
import inspect

from os.path import relpath, splitext
from importlib import import_module
from collections import defaultdict
from operator import methodcaller


from pytf.loaders import TestLoader, UnittestLoader
from pytf.core import Test, TestException, TestResult
from pytf.reporters import TextTestReporter, EarlyTextReporter
from pytf.contexts import StdCatcher
from pytf.finders import TestFinder

__all__ = ['TestLoader', 'UnittestLoader', 'Test', 'TextTestReporter']


class TestExecutor(object):

    def __init__(self, reporters=(), contexts=()):
        self.reporters = reporters
        self.contexts = contexts

    def _get_test_code_id(self, test):
        if inspect.ismethod(test.callback):
            return id(test.callback.im_func.func_code)
        elif inspect.isfunction(test.callback):
            return id(test.callback.func_code)

    def execute(self, test_suite):
        global_test_result = []
        # Start reporters
        map(methodcaller('begin_tests'), self.reporters)

        # Extract raw functions from test_suite
        test_code_ids = {self._get_test_code_id(test) for test in test_suite}

        # Run tests
        for test in test_suite:
            # Call contexts
            map(methodcaller('enter'), self.contexts)

            # Run test
            try:
                test()
            except TestException as test_exception:

                # Check if it's a dependency fail or not
                traceback = test_exception.exc_info[2]
                while traceback:
                    code_id = id(traceback.tb_frame.f_code)

                    if code_id in test_code_ids and code_id != self._get_test_code_id(test):
                        test_result = TestResult(test.id, test_exception, dependency_fail=True)
                        break
                    traceback = traceback.tb_next
                else:
                    # Not a dependency fail
                    test_result = TestResult(test.id, test_exception)
            else:
                test_result = TestResult(test.id)

            # Add each test message
            test_result.messages.extend(test.messages)

            # Call contexts end
            map(methodcaller('exit', test_result), self.contexts)

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
