from __future__ import print_function

import sys
import unittest

from pytf.contexts import StdCatcher

class StdContextTest(unittest.TestCase):

    def test_stdout_catch(self):
        std_catcher = StdCatcher()

        stdout_message = 'HI'
        stderr_message = 'Oups'

        std_catcher.enter()
        print(stdout_message)
        print(stderr_message, file=sys.stderr)
        get = std_catcher.exit({})

        expected = {'messages': [('Captured stdout', stdout_message + '\n'),
            ('Captured stderr', stderr_message + '\n')]}
        self.assertEqual(get, expected)
