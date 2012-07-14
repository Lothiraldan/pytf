

class Test(object):

    def __init__(self, callback, setup=None, tear_down=None):
        self.callback = callback
        self.setup = setup
        self.tear_down = tear_down

    def __call__(self):
        if self.setup:
            self.setup()
        self.callback()
        if self.tear_down:
            self.tear_down()
