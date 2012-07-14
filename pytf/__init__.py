from glob import iglob
from os.path import join

from loaders import TestLoader, UnittestLoader
from core import Test


class TestRunner(object):

    def __init__(self):
        self.loaders = {}

    def set_loaders(self, loaders):
        self.loaders = loaders

    def _load_modules(self, modules):
        levels = self.loaders.keys()
        levels.sort(reverse=True)

        for module in modules:
            for var in module.__dict__.values():
                for loader in self._iter_loaders(levels):
                    test = loader.load_object(var)

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

    def __init__(self, test_suite):
        self.test_suite = test_suite

    def execute(self):
        for test in self.test_suite:
            test()
