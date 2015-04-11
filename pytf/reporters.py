from __future__ import print_function

import sys
import time
import traceback


class BaseReporter(object):

    def begin_tests(self):
        pass

    def end_tests(self):
        pass



class TextTestReporter(BaseReporter):

    head_template = '{double_dash}\n{status}: {id}\n{single_dash}\n'
    message_template = '{title}\n{message}\n{single_dash}\n'
    message_foot_template = '{double_dash}\n'
    foot_template = '{status}: Ran {total} tests in {duration:.3f}s, ' \
                    '{failing} failing tests and {errors} ' \
                    'tests in errors. {dependencies} test in errors by dependency\n'
    start_template = 'Starting tests\n\n'

    def begin_tests(self):
        self.failed = []
        self.errors = []
        self.dependencies = []
        self.runs = 0
        self.start = time.time()
        self._print_tpl(self.start_template)

    def show_result(self, result):
        self.runs += 1
        if result.success:
            self._print('.')
        else:
            if result.exception.phase == 'test':
                if result.dependency_fail is False:
                    self._print('F')
                    self.failed.append(result)
                else:
                    self._print('D')
                    self.dependencies.append(result)
            else:
                self._print('E')
                self.errors.append(result)

    def end_tests(self):
        # Print a newline
        print('')

        self._print_results('ERROR', self.errors)
        self._print_results('FAILED', self.failed)
        self._print_results('DEPENDENCY', self.dependencies,
                            print_exception=False)

        print('')

        self._print_footer()


    def _print_results(self, status, results, **kwargs):
        for result in results:
            self._print_failing_test(status, result, **kwargs)

    def _print_failing_test(self, status, result, print_exception=True):
        double_dash = '=' * 70
        single_dash = '-' * 70

        self._print_tpl(self.head_template, double_dash=double_dash,
            single_dash=single_dash, status=status,
            id=result.id)

        if print_exception:
            traceback.print_exception(*result.exception.exc_info)

            for title, message in result.messages:
                self._print_tpl(self.message_template,
                    title='{:-^70}'.format(title),
                    message=message, single_dash=single_dash)

        self._print_tpl(self.message_foot_template, double_dash=double_dash)

    def _print_footer(self):
        stop = time.time()
        running_time = stop - self.start

        status = 'OK'

        if self.errors:
            status = 'ERROR'
        elif self.failed:
            status = 'FAILED'

        self._print_tpl(self.foot_template, total=self.runs,
                        duration=running_time, failing=len(self.failed),
                        errors=len(self.errors), status=status,
                        dependencies=len(self.dependencies))

    def _print_tpl(self, template, **kwargs):
        self._print(template.format(**kwargs))

    def _print(self, text):
        print(text, end='')
        sys.stdout.flush()


class EarlyTextReporter(TextTestReporter):

    success_template = '{status}: {id}\n'

    head_template = '\t{double_dash}\n\t{status}: {id}\n\t{single_dash}\n'
    message_template = '\t{title}\n\t{message}\n\t{single_dash}\n'
    message_foot_template = '\t{double_dash}\n'
    foot_template = '{status}: Ran {total} tests in {duration:.3f}s, ' \
                    '{failing} failing tests and {errors} ' \
                    'tests in errors\n'
    start_template = 'Starting tests\n\n'

    def show_result(self, result):
        self.runs += 1
        if result.success:
            self._print_tpl(self.success_template, status="OK", id=result.id)
        else:
            if result.exception.phase == 'test':
                self._print_failing_test("FAIL", result)
                self.failed.append(result)
            else:
                self._print_failing_test("ERROR", result)
                self.errors.append(result)

    def end_tests(self):
        # Print a newline
        print('')

        self._print_footer()
