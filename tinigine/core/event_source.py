# -*- coding:utf-8 -*-
"""
@author: ksf

@since: 2020/9/19 11:59 AM
"""

from tinigine.interface import AbstractEventSource
from tinigine.core.env import Environment
from tinigine.core.event import EventType
from tinigine.core.data_walker import DataWalker


class EventSource(AbstractEventSource):

    def __init__(self, env: Environment):
        super(EventSource, self).__init__(env)
        env.event_bus.add_event(env.data_proxy.on_subscribe, EventType.SUBSCRIBE)

    def events(self):
        return self.data_events()

    def data_events(self):
        env = self._env
        event_bus = env.event_bus
        start_date = self._env.params.start
        for data in DataWalker(self._env.data_proxy, start_date)


