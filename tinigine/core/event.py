# -*- coding:utf-8 -*-
"""
@author: ksf

@since: 2020-04-25 19:28
"""
from enum import Enum


class Event:
    def __init__(self, event_type, **kwargs):
        self.event_type = event_type
        self.__dict__.update(kwargs)

    def __str__(self):
        return str(self.__dict__)


class EventType(Enum):
    INITIALIZE = 'INITIALIZE'
    SUBSCRIBE = 'SUBSCRIBE'
    BEFORE_TRADING = 'BEFORE_TRADING'
    AFTER_TRADING = 'AFTER_TRADING'
    BAR = 'BAR'
    TICK = 'TICK'
    ORDER_NEW = 'ORDER_NEW'
    ORDER_CHANGE = 'ORDER_CHANGE'
    USER_EVENT = 'USER_EVENT'
    QUIT = 'QUIT'

