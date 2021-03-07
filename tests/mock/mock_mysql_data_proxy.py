"""
@project: tinigine
@author: kang 
@github: https://github.com/fsksf 
@since: 2021/3/6 1:20 AM
"""
import os
import pandas as pd
from tinigine.mod.data_from_tushare.data_proxy import MysqlDataProxy
from tests import TESTS_DIR


class MockMysqlDataProxy(MysqlDataProxy):

    def get_symbols(self):
        return ['000001.SZ', '600600.SH', '600703.SH']

    @staticmethod
    def get_calendar(start, end):
        calender_df = pd.read_csv(os.path.join(TESTS_DIR, 'data/quote/cn_daily_calender.csv'))
        del calender_df['id']
        calender_series = calender_df['timestamp'].sort_values()
        calender_series = calender_series[(calender_series >= start) & (calender_series <= end)]
        return calender_series.to_list()

    @staticmethod
    def get_factor(symbols, start, end):
        factor_df = pd.read_csv(os.path.join(TESTS_DIR, 'data/quote/cn_adj_factor.csv'))
        del factor_df['id']
        factor_df.sort_values('timestamp', inplace=True)
        factor_df = factor_df[(factor_df['timestamp'] >= start) & (factor_df['timestamp'] <= end)]
        return factor_df

    @staticmethod
    def get_quote(symbols, start, end):
        quote_df = pd.read_csv(os.path.join(TESTS_DIR, 'data/quote/cn_daily_stock_quote.csv'))
        quote_df.drop('id', axis=1, errors='ignore')
        quote_df.sort_values('timestamp', inplace=True)
        quote_df = quote_df[(quote_df['timestamp'] >= start) & (quote_df['timestamp'] <= end)]
        return quote_df
