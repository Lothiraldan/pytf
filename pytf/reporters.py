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
        if result.success:
            print('.', end='')
        else:
            if result.exception.phase == 'test':
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
            print("{0}: {1}".format(name, result.test_id))
            print("-" * 70)
            traceback.print_exception(*result.exception.exc_info)
            print("-" * 70)
            for message in result.messages:
                print(self._center_padding_format(70, message['title']))
                print(message['message'])
                print("-" * 70)
            print("\n")

    @staticmethod
    def _center_padding_format(cols, string, padding_char='-'):
        length = (cols - len(string)) / 2.

        if length.is_integer():
            # len(string) is #PAIR
            return '{0}{1}{0}'.format(padding_char * length, string)
        else:
            data = (padding_char * (int(length) + 1), string,
                padding_char * int(length))
            return '{0}{1}{2}'.format(*data)
