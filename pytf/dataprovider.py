from .loaders import TestGenerator


def call(*args, **kwargs):
    return args, kwargs


def DataProvider(**datas):
    def wrapper(func):
        generator = _DataProviderGenerator(datas)
        loaders = getattr(func, 'loaders', [])
        loaders.append(generator)
        func.loaders = loaders
        return func
    return wrapper


class _DataProviderGenerator(object):

    def __init__(self, calls):
        self.calls = calls

    def load_function(self, function):
        return self._gen_generators(function, 'function')

    def load_method(self, method):
        return self._gen_generators(method, 'method')

    def load_class(self, klass):
        return self._gen_generators(klass, 'class')

    def _gen_generators(self, test_callback, type):
        generators = []
        for call_name, call_args in self.calls.items():
            message = '%s has been called with: %s' % (type.capitalize(),
                call_args,)
            generator = TestGenerator(call_name, args=call_args,
                messages=[('Call args', message)])
            generators.append(generator)
        return generators


def CallGenerator(arg_name, **arg_values):
    def wrapper(func):
        generator = _CallGenerator(arg_name, arg_values)
        loaders = getattr(func, 'loaders', [])
        loaders.append(generator)
        func.loaders = loaders
        return func
    return wrapper


class _CallGenerator(object):

    def __init__(self, arg_name, arg_values):
        self.arg_name = arg_name
        self.arg_values = arg_values

    def load_function(self, function):
        return self._gen_generators(function, 'function')

    def load_method(self, function):
        return self._gen_generators(function, 'method')

    def _gen_generators(self, test_callback, type):
        generators = []
        for call_name, arg_value in self.arg_values.items():
            message = '%s has been called with: %s=%s' % (type.capitalize(),
                self.arg_name, arg_value,)
            generator = TestGenerator(call_name,
                messages=[('Call args', message)],
                args=((), {self.arg_name: arg_value}))
            generators.append(generator)
        return generators
