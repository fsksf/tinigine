# -*- coding:utf-8 -*-
"""
@author: ksf

@since: 2020-04-25 17:44
"""


class Strategy:

    def __init__(self, env, algo_text, algo_file=None, log_level='INFO'):
        self._env = env
        self._event_bus = env.event_bus
        self._initialize = None
        self._before_trade = None
        self._on_order_change = None
