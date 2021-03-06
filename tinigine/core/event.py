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
    ORDER_NEW = 'ORDER_NEW'                                         # 创建订单
    ORDER_SUBMISSION = 'ORDER_SUBMISSION'                           # 校验订单
    ORDER_SUBMISSION_PASSED = 'ORDER_SUBMISSION_PASSED'
    ORDER_SUBMISSION_REJECTED = 'ORDER_SUBMISSION_REJECTED'
    ORDER_CANCELLATION = 'ORDER_CANCELLATION'
    ORDER_CANCELLATION_PASSED = 'ORDER_CANCELLATION_PASSED'
    ORDER_CANCELLATION_REJECTED = 'ORDER_CANCELLATION_REJECTED'
    ORDER_CHANGE = 'ORDER_CHANGE'
    ORDER_FILLING = 'ORDER_FILLING '
    ORDER_FILLING_PASSED = 'ORDER_FILLING_PASSED'
    ORDER_REJECTED = 'ORDER_REJECTED'
    ORDER_DEAL = 'ORDER_DEAL'
    SETTLEMENT = 'SETTLEMENT'
    USER_EVENT = 'USER_EVENT'
    QUIT = 'QUIT'

