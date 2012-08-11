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
        stdout = self.stdout.getvalue()
        if stdout:
            test_result.add_message('Captured stdout', stdout)
        stderr = self.stderr.getvalue()
        if stderr:
            test_result.add_message('Captured stderr', stderr)
