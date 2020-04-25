# -*- coding:utf-8 -*-
"""
@author: ksf

@since: 2020-04-25 17:48
"""

from collections import defaultdict
from functools import wraps

class EventBus:

    def __init__(self):
        self._events_register_dict = defaultdict(list)

    def add_event(self, func, event):
        self._events_register_dict[event].append(func)

    def get_event_funcs(self, event):
        for func in self._events_register_dict[event]:
            yield func

    def on(self, event):
        def outer(func):
            self.add_event(func, event)

            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return outer

    def emit(self, event, *args, **kwargs):
        for func in self.get_event_funcs(event):
            func(event, *args, **kwargs)

    def emit_after(self, event):
        def outer(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                self.emit(event)
                return result
            return wrapper
        return outer
