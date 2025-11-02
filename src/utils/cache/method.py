def cached(func):
    """
    Caches the result of a method call.
    """
    cache = {}
    def wrapper(self, *args):
        if args in cache:
            return cache[args]
        result = func(self, *args)
        cache[args] = result
        return result
    return wrapper