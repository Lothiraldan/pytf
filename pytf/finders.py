from os.path import join, isdir, isfile
from os import listdir
from glob import iglob


class TestFinder(object):

    def __init__(self, path, pattern=None):
        if pattern is None:
            pattern = 'test*.py'
        self.path = path
        self.pattern = pattern

    def find(self, path=None):
        if not path:
            path = self.path

        for full_path in iglob(join(path, self.pattern)):
            if full_path.endswith('__init__.py'):
                continue
            else:
                yield full_path

        for directory in filter(lambda d: isdir(join(path, d)), listdir(path)):

            if not isfile(join(path, directory, '__init__.py')):
                continue

            for test_file in self.find(join(path, directory)):
                yield test_file
