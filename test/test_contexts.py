from __future__ import print_function

import sys
import unittest

from pytf.contexts import StdCatcher
from pytf.core import TestResult

class StdContextTest(unittest.TestCase):

    def test_stdout_catch(self):
        std_catcher = StdCatcher()

        stdout_message = 'HI'
        stderr_message = 'Oups'

        result = TestResult('test_id')

        std_catcher.enter()
        print(stdout_message)
        print(stderr_message, file=sys.stderr)
        std_catcher.exit(result)

        expected = [{'title': 'Captured stdout', 'message': stdout_message +
            '\n'}, {'title': 'Captured stderr', 'message': stderr_message +
            '\n'}]
        self.assertEqual(result.messages, expected)
