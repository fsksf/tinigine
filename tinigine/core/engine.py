# -*- coding:utf-8 -*-
"""
@author: ksf

@since: 2020-04-25 17:44
"""
import sys
import os
from importlib import import_module
from tinigine.core.env import Environment
from tinigine.core.event import Event, EventType


class Engine:

    def __init__(self, env: Environment):
        self._env = env
        self._mod_list = []

    def initialize(self):
        self._env.event_bus.emit(Event(EventType.INITIALIZE))

    def load_mod(self):
        mod_names = self._env.conf.get_config()['mod']
        for mod_name in mod_names:
            mod = self._import_mod(mod_name)
            if mod:
                self._mod_list.append(mod.load())

    def _import_mod(self, name):
        try:
            self._env.logger.info(f'loading mod: {name} from standard path')
            mod = import_module(f'tinigine.mod.{name}')
        except ImportError:
            self._env.logger.info(f'standard path not fund')
            try:
                custom_dir = os.path.join(self._env.conf.get_mod_custom_dir(), 'mods')
                if sys.path.index(custom_dir) < 0:
                    sys.path.insert(0, custom_dir)
                mod = import_module(mod)
            except ImportError:
                self._env.logger.error(f'mod_import_error: {mod}')
                return None
        return mod

    def run(self):
        event_bus = self._env.event_bus
        event_source = self._env.event_source
        self.initialize()
        self.set_up()
        for event in event_source.events():
            event_bus.emit(event)
        if self._env.metrics:
            self._env.metrics.get_result()
        self.tear_down()

    def set_up(self):
        for mod in self._mod_list:
            mod.set_up(env=self._env)

    def tear_down(self):
        for mod in self._mod_list:
            mod.tear_down()
