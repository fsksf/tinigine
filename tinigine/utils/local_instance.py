import threading
context = threading.local()
import tinigine.api


def get_instance(name):
    return getattr(context, name, None)


def set_instance(name, obj):
    setattr(context, name, obj)


class InstanceApiDecorator:

    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)

    def __init__(self, func):
        self._func = func
        tinigine.api.__all__.append(func.__name__)
        setattr(tinigine.api, func.__name__, self._func)

    def __get__(self, instance, owner):
        """
        :param instance: first argument as the instance of owner
        :param owner:
        :return:
        """
        from functools import partial
        self.__self__ = instance
        print(self, instance, owner)
        return partial(self, instance)
