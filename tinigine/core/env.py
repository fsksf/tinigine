# -*- coding:utf-8 -*-
"""
@author: ksf

@since: 2020-04-25 17:44
"""


class Environment:
    def __init__(self, params):
        self.params = params
        self.data_proxy = None
        self.event_source = None
        self.portfolio_manager = None
        self.broker = None
        self.metrics = None

    def set_event_source(self, event_source):
        self.event_source = event_source

    def set_portfolio_manager(self, portfolio_manager):
        self.portfolio_manager = portfolio_manager
