# -*- coding:utf-8 -*-
"""
@author: ksf

@since: 2020/9/19 11:59 AM
"""
from tinigine.interface import AbstractEventSource, AbstractEnv
from tinigine.core.env import Environment
from tinigine.core.event import EventType, Event


class EventSource(AbstractEventSource):

    def __init__(self, env: AbstractEnv):
        self._env = env

    def events(self):
        return self.data_events()

    def data_events(self):
        yield Event(event_type=EventType.INITIALIZE)
        for data in self._env.data_proxy.data_walker:
            # 每天先完成上个交易日下单的撮合成交
            yield Event(event_type=EventType.ORDER_DEAL)
            yield Event(event_type=EventType.BEFORE_TRADING, data=data)
            yield Event(event_type=EventType.BAR, data=data)
            # 当前Bar订单提交
            yield Event(event_type=EventType.SETTLEMENT)

