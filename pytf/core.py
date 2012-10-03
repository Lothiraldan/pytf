import sys

from collections import Iterable, Mapping


class TestResult(object):

    def __init__(self, test_id, exception=None):
        self.test_id = test_id
        if not exception:
            self.success = True
        else:
            self.success = False
        self.exception = exception
        self.messages = []

    def add_message(self, title, message):
        self.messages.append((title, message))

    def __cmp__(self, other):
        return cmp(self.__dict__, other.__dict__)


class Test(object):

    def __init__(self, test_id, callback, set_up=None, tear_down=None):
        self.test_id = test_id
        self.callback = callback

        if set_up and not isinstance(set_up, Iterable):
            set_up = (set_up,)
        self.set_up = set_up

        if tear_down and not isinstance(tear_down, Iterable):
            tear_down = (tear_down,)
        self.tear_down = tear_down
        self.messages = []

    def add_message(self, title, message):
        self.messages.append((title, message))

    def __call__(self):
        args = {}
        if self.set_up:
            for set_up in self.set_up:
                return_value = self._execute(set_up, 'set_up')

                if return_value and getattr(set_up, 'pass_return_value', False):
                    if isinstance(return_value, Mapping):
                        args.update(return_value)

        self._execute(self.callback, 'test', args)

        if self.tear_down:
            for tear_down in self.tear_down:
                self._execute(tear_down, 'tear_down')

    def _execute(self, callback, phase, args = None):
        try:
            if args:
                return callback(**args)
            else:
                return callback()
        except Exception as e:
            raise TestException("Exception during %s" % phase, self.test_id,
                callback, phase, e, sys.exc_info())

    def __eq__(self, test):
        return self.__dict__ == test.__dict__

    def __repr__(self):
        return 'Test(%s)' % self.__dict__


class TestException(Exception):
    def __init__(self, msg, test_id, callable, phase, exception, exc_info):
        super(TestException, self).__init__(self, msg)
        self.test_id = test_id
        self.callable = callable
        self.phase = phase
        self.exception = exception
        self.exc_info = exc_info
