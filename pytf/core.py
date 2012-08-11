import sys


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
        self.messages.append({'title': title, 'message': message})

    def __cmp__(self, other):
        return cmp(self.__dict__, other.__dict__)


class Test(object):

    def __init__(self, test_id, callback, set_up=None, tear_down=None):
        self.test_id = test_id
        self.callback = callback
        self.set_up = set_up
        self.tear_down = tear_down

    def __call__(self):
        if self.set_up:
            self._execute(self.set_up, 'set_up')

        self._execute(self.callback, 'test')

        if self.tear_down:
            self._execute(self.tear_down, 'tear_down')

    def _execute(self, callback, phase):
        try:
            callback()
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
