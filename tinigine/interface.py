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
        """
        订阅
        :param event:
        :return:
        """
        raise NotImplementedError

    def get_calendar(self):
        """
        获取交易日历
        :return:
        """
        raise NotImplementedError

    def get_contract_info(self, symbol):
        raise NotImplementedError

    def get_symbols(self):
        raise NotImplementedError

    def get_datetime(self):
        """
        获取策略运行的当前时间
        :return: dt
        """
        raise NotImplementedError


class AbstractEventSource:

    def __init__(self, env):
        self._env = env

    def events(self):
        raise NotImplementedError


class AbstractMetrics:

    def get_result(self):
        raise NotImplementedError
