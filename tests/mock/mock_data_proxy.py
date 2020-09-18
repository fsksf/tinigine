# -*- coding:utf-8 -*-
"""
@author: ksf

@since: 2020/8/27 8:16 AM
"""
import pandas as pd
from tinigine.interface import AbstractDataProxy
from tinigine.core.contract import StockContract
from tinigine.core.frame import Frame, SFrame


class MockDataProxy(AbstractDataProxy):

    def __init__(self):
        self._cache = None
        self._csv_path = '../data/quote/cn_daily_stock_quote.csv'
        quote_data = pd.read_csv(self._csv_path)
        self._symbols = list(set(quote_data['symbol']))
        self._calendar = sorted(set(quote_data['timestamp']))
        self._quote_data = quote_data.set_index(['timestamp', 'symbol'])
        self._quote_data.sort_index(inplace=True)

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
            fr = Frame(data.to_numpy(), data.index, data.columns)
            sf.add(fr)
        self._cache = sf
