# -*- coding:utf-8 -*-
"""
@author: ksf

@since: 2020-04-25 17:44
"""
from tinigine.interface import AbstractDataProxy
from tinigine.core.event_bus import EventBus
from tinigine.utils.logger import get_logger


class Environment:
    def __init__(self, params):
        self.params = params
        self.data_proxy: AbstractDataProxy = AbstractDataProxy()
        self.event_source = None
        self.event_bus = EventBus()
        self.portfolio_manager = None
        self.broker = None
        self.metrics = None
        self.logger = get_logger(log_type='system', level=params.log_level)

    def set_event_source(self, event_source):
        self.event_source = event_source

    def set_portfolio_manager(self, portfolio_manager):
        self.portfolio_manager = portfolio_manager

    def set_data_proxy(self, data_proxy):
        self.data_proxy = data_proxy