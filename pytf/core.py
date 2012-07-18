import sys


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


class TestException(Exception):
    def __init__(self, msg, test_id, callable, phase, exception, exc_info):
        super(TestException, self).__init__(self, msg)
        self.test_id = test_id
        self.callable = callable
        self.phase = phase
        self.exception = exception
        self.exc_info = exc_info
