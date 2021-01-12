# -*- coding:utf-8 -*-
"""
@author: ksf

@since: 2020-04-25 17:12
"""
from collections import defaultdict


class AbstractModule:

    def set_up(self, env):
        raise NotImplementedError

    def tear_down(self):
        raise NotImplementedError


class AbstractDataProxy:

    def __init__(self, env):
        self._env = env

    def get_sf(self):
        raise NotImplementedError

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

    def subscribe(self, symbols, before_bar_count=1):
        raise NotImplementedError


class AbstractEventSource:

    def __init__(self, env):
        self._env = env

    def events(self):
        raise NotImplementedError


class AbstractMetrics:

    def get_result(self):
        raise NotImplementedError


class AbstractEventBus:

    def __init__(self):
        self._events_register_dict = defaultdict(list)

    def add_event(self, func, event_type):
        self._events_register_dict[event_type].append(func)

    def get_event_funcs(self, event_type):
        return self._events_register_dict[event_type]

    def emit(self, event, *args, **kwargs):
        pass


class AbstractEnv:
    def __init__(self, params):
        self.params = params
        self.data_proxy: AbstractDataProxy = AbstractDataProxy(self)
        self.event_source: AbstractEventSource = AbstractEventSource(self)
        self.event_bus: AbstractEventBus = AbstractEventBus()
        self.portfolio_manager = None
        self.broker = None
        self.metrics = None
        self.logger = None
        self.strategy = None

    def set_event_source(self, event_source):
        self.event_source = event_source

    def set_portfolio_manager(self, portfolio_manager):
        self.portfolio_manager = portfolio_manager

    def set_data_proxy(self, data_proxy):
        self.data_proxy = data_proxy
