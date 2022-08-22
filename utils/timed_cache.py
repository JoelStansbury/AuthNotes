import time
from types import FunctionType


class TimedCache:
    CACHE = {}

    def __init__(self, maxsize=128, default_timeout=0):
        self.default_timeout = default_timeout
        self.maxsize = maxsize

    def prune_cache(self, maxsize=128):
        if len(self.CACHE) > maxsize:
            to_delete = sorted(self.CACHE.items(), key=lambda x: x[1])[
                : maxsize - len(self.CACHE)
            ]
            for k, v in to_delete:
                self.CACHE.pop(k)

    def __call__(self, timeout=None):
        no_params = False
        if isinstance(timeout, FunctionType):
            no_params = True
            func = timeout
            timeout = self.default_timeout
        if timeout is None:
            timeout = self.default_timeout

        def inner(func):
            def wrapper(*args, **kwargs):
                key = (func.__name__, str(args), str(sorted(list(kwargs.items()))))
                if key in self.CACHE:
                    deathtime, value = self.CACHE[key]
                    if deathtime > time.time():
                        return value
                self.CACHE[key] = (time.time() + timeout, func(*args, **kwargs))
                self.prune_cache()
                return self.CACHE[key][1]

            return wrapper

        if no_params:
            return inner(func)

        return inner