# -*- coding:utf-8 -*-
"""
@author: ksf

@since: 2020-04-25 17:28
"""


class StockContract:

    __slots__ = ['symbol', 'currency', 'exchange', 'lot_size', 'name']

    def __init__(self,
                 symbol,
                 currency,
                 exchange,
                 lot_size=None,
                 name=None):
        self.symbol = symbol
        self.currency = currency
        self.exchange = exchange
        self.lot_size = lot_size
        self.name = name


