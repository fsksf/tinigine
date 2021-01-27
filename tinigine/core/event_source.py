# -*- coding:utf-8 -*-
"""
@author: ksf

@since: 2020/9/19 11:59 AM
"""
from tinigine.interface import AbstractEventSource
from tinigine.core.env import Environment
from tinigine.core.event import EventType, Event
from tinigine.core.data_walker import DataWalker


class EventSource(AbstractEventSource):

    def __init__(self, env: Environment):
        super(EventSource, self).__init__(env)

    def events(self):
        return self.data_events()

    def data_events(self):
        env = self._env
        event_bus = env.event_bus
        start_date = env.params.start
        yield Event(event_type=EventType.INITIALIZE)
        for data in DataWalker(env.data_proxy.get_sf(), start_date):
            yield Event(event_type=EventType.BAR, data=data)


