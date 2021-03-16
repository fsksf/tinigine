# -*- coding:utf-8 -*-
"""
@author: ksf

@since: 2020-04-25 17:44
"""
from tinigine.interface import AbstractDataProxy, AbstractEnv
from tinigine.core.params import Params
from tinigine.core.event_bus import EventBus
from tinigine.core.strategy import Strategy
from tinigine.utils.logger import get_logger
from tinigine.config import conf


class Environment(AbstractEnv):
    def __init__(self, params: Params):
        self.params = params
        self.data_proxy: AbstractDataProxy = AbstractDataProxy(self)
        self.event_source = None
        self.event_bus = EventBus()
        self.portfolio_manager = None
        self.broker = None
        self.engine = None
        self.metrics = None
        self.logger = get_logger(log_type='system', level=params.log_level)
        self.strategy = Strategy(env=self, algo_text=params.algo_text, log_level=params.log_level)
        self.conf = conf
        self.logger.info(str(params))
