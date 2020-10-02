# -*- coding:utf-8 -*-
"""
@author: ksf

@since: 2020-04-25 17:44
"""
from datetime import datetime
from tinigine.core.constant import Freq, Currency, Market, FREQ_FORMAT_DICT


class Params:
    def __init__(self, algo_text='', algo_file=None, capital=None, start=None, end=None, freq=None, market=None,
                 currency=None, log_level='INFO'):
        self.freq = Freq(freq)
        self.start = start
        self.end = end

        self.currency = Currency(currency)
        self.market = Market(market)

        self.algo_file = algo_file

        if not algo_text and algo_file:
            with open(algo_file, 'r') as f:
                algo_text = f.read()
        self.algo_text = algo_text
        self.capital = capital
        self.log_level = log_level

    def set_algo(self, algo_text):
        self.algo_text = algo_text