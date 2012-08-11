import sys

from StringIO import StringIO


class StdCatcher(object):

    def enter(self):
        self.stdout = StringIO()
        self.old_stdout = sys.stdout
        sys.stdout = self.stdout

        self.stderr = StringIO()
        self.old_stderr = sys.stderr
        sys.stderr = self.stderr

    def exit(self, test_result):
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr
        return {'messages': [('Captured stdout', self.stdout.getvalue()),
            ('Captured stderr', self.stderr.getvalue())]}
