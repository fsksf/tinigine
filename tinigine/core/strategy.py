# -*- coding:utf-8 -*-
"""
@author: ksf

@since: 2020-04-25 17:44
"""

from .env import Environment
from tinigine.utils.logger import get_logger

class Strategy:

    def __init__(self, env: Environment, algo_text, log_level='INFO'):
        self._env = env
        self._event_bus = env.event_bus
        self._initialize = None
        self._before_trade = None
        self._on_order_change = None
        self.logger = self._env.logger
        self._on_bar = None

        self._user_space = dict()
        self.add_api('log', get_logger())

    def add_api(self, name, obj):
        self._user_space[name] = obj

