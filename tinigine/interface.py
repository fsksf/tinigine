# -*- coding:utf-8 -*-
"""
@author: ksf

@since: 2020-04-25 17:12
"""


class AbstractModule:

    def set_up(self, env):
        raise NotImplementedError

    def tear_down(self):
        raise NotImplementedError


class AbstractDataProxy:

    def on_subscribe(self, event):
        raise NotImplementedError

    def get_calendar(self):
        raise NotImplementedError

    def get_contract_info(self, symbol):
        raise NotImplementedError

    def get_symbols(self):
        raise NotImplementedError


class AbstractEventSource:

    def __init__(self, env):
        self._env = env

    def events(self):
        raise NotImplementedError


class AbstractMetrics:

    def get_result(self):
        raise NotImplementedError
