# -*- coding:utf-8 -*-
"""
@author: ksf

@since: 2020-04-25 17:44
"""

from tinigine.core.env import Environment
from tinigine.core.event import Event, EventType


class Engine:

    def __init__(self, env: Environment):
        self._env = env
        self._mod_list = []

    def initialize(self):
        self._env.event_bus.emit(Event(EventType.INITIALIZE))

    def run(self):
        event_bus = self._env.event_bus
        event_source = self._env.event_source

        for event in event_source.events():
            event_bus.emit(event)

        self.tear_down()

        return self._env.metrics.get_result()

    def set_up(self):
        for mod in self._mod_list:
            mod.set_up(env=self._env)

    def tear_down(self):
        for mod in self._mod_list:
            mod.tear_down()
