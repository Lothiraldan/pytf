from __future__ import print_function

import time
import traceback


class BaseReporter(object):

    def begin_tests(self):
        pass

    def end_tests(self):
        pass


class TextTestReporter(BaseReporter):

    def begin_tests(self):
        self.failed = []
        self.errors = []
        self.runs = 0
        self.start = time.time()

    def show_result(self, result):
        self.runs += 1
        if result['success']:
            print('.', end='')
        else:
            if result['exception'].phase == 'test':
                print('F', end='')
                self.failed.append(result)
            else:
                print('E', end='')
                self.errors.append(result)

    def end_tests(self):
        stop = time.time()
        # Print a newline
        print('')

        self._print('ERROR', self.errors)
        self._print('FAIL', self.failed)

        running_time = stop - self.start
        print("Ran {} tests in {:.3f}s".format(self.runs, running_time))

    def _print(self, name, results):
        for result in results:
            print("=" * 70)
            print("{0}: {1}".format(name, result['test_id']))
            print("-" * 70)
            traceback.print_exception(*result['exception'].exc_info)
            print("-" * 70)
            print("\n")
