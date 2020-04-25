# -*- coding:utf-8 -*-
"""
@author: ksf

@since: 2020-04-25 19:28
"""
from enum import Enum


class Event:
    def __init__(self, event_type, **kwargs):
        self.type = event_type
        self.__dict__.update(kwargs)

    def __str__(self):
        return str(self.__dict__)


class EventType(Enum):
    INITIALIZE = 'initialize'
    BEFORE_TRADING = 'before_trading'
    AFTER_TRADING = 'after_trading'
    BAR = 'bar'
    DATA = 'data'

