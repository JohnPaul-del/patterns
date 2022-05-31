from time import time
from .creational_patterns import Logger


class Routes:

    def __init__(self, routes: dict, url: str):
        self.routes = routes
        self.url = url


    def __call__(self, cls):
        self.routes[self.url] = cls()


class Debugging:

    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        def time_decorator(func):
            def wrapper(*args, **kwargs):
                start_time=time()
                func_result = func(*args, **kwargs)
                interval = time() - start_time

                Logger.log(f'Debug info: {self.name} has spent {interval}')
                return func_result
            return wrapper
        return time_decorator(cls)
