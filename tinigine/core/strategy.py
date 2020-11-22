# -*- coding:utf-8 -*-
"""
@author: ksf

@since: 2020-04-25 17:44
"""

from .env import Environment
from .event import EventType, Event
from tinigine.utils.logger import get_logger


class Strategy:

    def __init__(self, env: Environment, algo_text, log_level='INFO'):
        self._env = env
        self._event_bus = env.event_bus
        self._initialize = None
        self._subscribe = None
        self._before_trade = None
        self._on_order_changed = None
        self._on_event = None
        self._on_bar = None
        self._on_tick = None
        self.logger = self._env.logger
        self._algo_text = algo_text

        self._user_space = dict()
        self.add_api('log', get_logger())

    def add_api(self, name, obj):
        self._user_space[name] = obj

    def init_algo(self):
        exec(self._algo_text, self._user_space)

    def on_quit(self):
        # TODO 标准处理+自定义
        user_quit = self._user_space.get('on_quit', None)
        if user_quit:
            user_quit()

    def parse_strategy(self):
        self._initialize = self._user_space.get('initialize', None)
        self._before_trade = self._user_space.get('before_trade', None)
        self._on_bar = self._user_space.get('on_bar', None)
        self._on_tick = self._user_space.get('on_tick', None)
        self._on_order_changed = self._user_space.get('on_order_changed', None)
        self._on_event = self._user_space.get('on_event', None)

        # ------- add stand event -------
        if self._initialize:
            self._event_bus.add_event(self._initialize, EventType.INITIALIZE)
        if self._subscribe:
            self._event_bus.add_event(self._env.data_proxy.on_subscribe, EventType.SUBSCRIBE)
        if self._before_trade:
            self._event_bus.add_event(self._before_trade, EventType.BEFORE_TRADING)
        if self._on_bar:
            self._event_bus.add_event(self._on_bar, EventType.BAR)
        if self._on_tick:
            self._event_bus.add_event(self._on_tick, EventType.TICK)
        if self._on_order_changed:
            self._event_bus.add_event(self._on_order_changed, EventType.ORDER_CHANGE)
        if self._on_event:
            self._event_bus.add_event(self._on_event, EventType.USER_EVENT)

        self._event_bus.add_event(self.on_quit, EventType.QUIT)

        # ------- emit event --------
        self._event_bus.emit(Event(EventType.INITIALIZE))
        self._event_bus.emit(Event(EventType.SUBSCRIBE))
