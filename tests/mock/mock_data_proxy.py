# -*- coding:utf-8 -*-
"""
@author: ksf

@since: 2020/8/27 8:16 AM
"""
import os
import pandas as pd
from tinigine.utils.utils import local_method, instance_api_decorator
from tinigine.interface import AbstractDataProxy
from tinigine.core.contract import StockContract
from tinigine.core.event import Event, EventType
from tinigine.core.frame import Frame, SFrame
from tests import TESTS_DIR


class MockDataProxy(AbstractDataProxy):

    def __init__(self, env):
        self._env = env
        self._cache = None
        self._csv_path = os.path.join(TESTS_DIR, 'data/quote/cn_daily_stock_quote.csv')
        quote_data = pd.read_csv(self._csv_path)
        self._symbols = list(set(quote_data['symbol']))
        self._calendar = sorted(set(quote_data['timestamp']))
        self._quote_data = quote_data.set_index(['timestamp', 'symbol'])
        self._quote_data.sort_index(inplace=True)
        # 订阅行情function 关联 订阅 事件
        self._env.event_bus.on(EventType.SUBSCRIBE)(self.on_subscribe)

    def get_sf(self):
        return self._cache

    def get_calendar(self, start, end):
        s = e = None
        for i, d in enumerate(self._calendar):
            if s is None and d >= start:
                s = i
            if d <= e:
                e = i
            if e is not None:
                e += 1
        return self._calendar[s:e]

    def get_contract_info(self, symbol):
        return StockContract(
            symbol, 'CNY', 'SH', 100
        )

    def get_symbols(self):
        return self._symbols

    def on_subscribe(self, event):
        symbols = event.symbols
        sf = SFrame()
        for field in self._quote_data.columns:
            data = self._quote_data[field]
            data = data.unstack()
            fr = Frame(data.to_numpy(), list(data.index), name=field, columns=list(data.columns))
            sf.add(fr)
        self._cache = sf
        return sf

    def subscribe(self, symbols, before_bar_count=1):

        evt = Event(event_type=EventType.SUBSCRIBE, symbols=symbols, before_bar_count=before_bar_count)
        self._env.event_bus.emit(event=evt)

