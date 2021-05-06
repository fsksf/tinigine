# -*- coding:utf-8 -*-
"""
@author: ksf

@since: 2020-04-25 17:44
"""

from tinigine.interface import AbstractEnv, AbstractEventBus
from .event import EventType, Event
from tinigine.utils.logger import get_logger
from tinigine.utils.local_instance import set_instance
from tinigine.utils.utils import local_method, add_api_method
from tinigine.core.context import Context


class Strategy:

    def __init__(self, env: AbstractEnv, algo_text, log_level='INFO'):
        self._env: AbstractEnv = env
        self._event_bus: AbstractEventBus = env.event_bus
        self._initialize = None
        self._subscribe = None
        self._before_trade = None
        self._on_order_changed = None
        self._on_event = None
        self._on_bar = None
        self._on_tick = None
        self.logger = self._env.logger
        self._algo_text = algo_text
        self._context = Context()

        self._user_space = dict()
        self.add_api('log', get_logger())

    def set_up(self):
        """
        策略的初始化应该在所有mod初始化之后
        :return:
        """
        add_api_method(self.subscribe)
        self.init_algo()
        self.parse_strategy()

    def tear_down(self):
        pass

    def add_api(self, name, obj):
        self._user_space[name] = obj

    def init_algo(self):
        exec(self._algo_text, self._user_space)

    def on_quit(self):
        # TODO 标准处理+自定义
        user_quit = self._user_space.get('on_quit', None)
        if user_quit:
            user_quit()

    def initialize(self, event):
        self._initialize(self._context)

    def on_bar(self, event):
        self._on_bar(self._context, event.data)

    def before_trade(self, event):
        self._before_trade(self._context, event.data)

    def on_order_change(self, event):
        self._on_order_changed(self._context, event.order)

    def parse_strategy(self):
        self._initialize = self._user_space.get('initialize', None)
        self._before_trade = self._user_space.get('before_trade', None)
        self._on_bar = self._user_space.get('on_bar', None)
        self._on_tick = self._user_space.get('on_tick', None)
        self._on_order_changed = self._user_space.get('on_order_changed', None)
        self._on_event = self._user_space.get('on_event', None)

        # ------- add stand event -------
        if self._initialize:
            self._event_bus.add_event(self.initialize, event_type=EventType.INITIALIZE)
        if self._before_trade:
            self._event_bus.add_event(self.before_trade, event_type=EventType.BEFORE_TRADING)
        if self._on_bar:
            self._event_bus.add_event(self.on_bar, event_type=EventType.BAR)
            self._event_bus.add_event(self.on_order_change, event_type=EventType.ORDER_CHANGE)
        if self._on_event:
            self._event_bus.add_event(self._on_event, event_type=EventType.USER_EVENT)

        self._event_bus.add_event(self.on_quit, event_type=EventType.QUIT)

        # ------- emit event --------

    def subscribe(self, symbols, before_bar_count=1):
        self._env.data_proxy.subscribe(symbols=symbols, before_bar_count=before_bar_count)
