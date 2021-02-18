# -*- coding:utf-8 -*-
"""
@author: ksf

@since: 2019-10-29 08:55
"""
import time
import tushare
from functools import lru_cache
from requests.exceptions import ConnectionError
import pandas as pd
from tinigine.core.constant import Market
from tinigine.mod.data_from_tushare import mod_conf


tushare.set_token(mod_conf.get_config()['token'])

ts_pro = tushare.pro_api()


class DataUtilFromTushare:

    @staticmethod
    def query(api_name, fields='', **kwargs):
        retry_count = 0
        retry = 5
        ts_code = kwargs.get('ts_code', None)
        if ts_code is not None and isinstance(ts_code, (list, tuple)):
            kwargs['ts_code'] = ','.join(ts_code)

        while retry_count < retry:
            time.sleep(0.6)
            retry_count += 1
            try:
                single = ts_pro.query(api_name, fields, **kwargs)
                return single
            except ConnectionError as e:
                if retry_count == retry:
                    raise
                else:
                    time.sleep(3)

    @staticmethod
    @lru_cache(4)
    def load_basic(market=Market.CN):
        if market == Market.CN:
            contracts = ts_pro.stock_basic(list_status='L')
            contracts.rename({'symbol': 'code', 'ts_code': 'symbol', 'market': 'board'}, inplace=True, axis=1)
            contracts['market'] = market.name
        else:
            raise NotImplementedError
        return contracts

    @staticmethod
    def load_daily_hists_v(codes, start_date, end_date, market=Market.CN):
        quote_list = []
        if market == Market.CN:
            for code in codes:
                single = DataUtilFromTushare.query('daily', ts_code=code, start_date=start_date, end_date=end_date)
                quote_list.append(single[['ts_code', 'trade_date', 'open', 'high', 'low', 'close', 'vol']])
        else:
            raise NotImplementedError

        data = pd.concat(quote_list, ignore_index=True)
        data.rename({'ts_code': 'symbol', 'vol': 'volume'}, inplace=True, axis=1)
        return data

    @staticmethod
    def load_daily_hists_h(codes=None, trade_dates=None, market=None):

        quote_list = []
        if isinstance(codes, list):
            ts_codes = ','.join(codes)
        else:
            ts_codes = codes
        if market == Market.CN:
            for trade_date in trade_dates:
                single = DataUtilFromTushare.query('daily', ts_code=ts_codes, trade_date=trade_date)
                quote_list.append(single[['ts_code', 'trade_date', 'open', 'high', 'low', 'close', 'vol']])
        else:
            raise NotImplementedError

        data = pd.concat(quote_list, ignore_index=True)
        data.rename({'ts_code': 'symbol', 'vol': 'volume'}, inplace=True, axis=1)
        return data

    @staticmethod
    def load_calendar(start_date=None, end_date=None, market=Market.CN):
        if market == Market.CN:
            calendar = ts_pro.trade_cal(start_date=start_date, end_date=end_date, is_open=1)['cal_date'].to_list()
            return [int(c) for c in calendar]
        else:
            raise NotImplementedError

    @staticmethod
    def load_adj_factors(symbols=None, start_date=None, end_date=''):
        df = DataUtilFromTushare.query('adj_factor', ts_code=symbols, start_date=start_date, end_date=end_date)
        mask = df['adj_factor'].pct_change() != 0.0
        df = df.loc[mask]
        df.rename({'ts_code': 'symbol', 'trade_date': 'timestamp'}, inplace=True, axis=1)
        return df


if __name__ == '__main__':
    symbols = DataUtilFromTushare.load_basic()
    print(symbols.iloc[0])
    symbols = symbols.iloc[:5, 0]
    print(symbols)
    quote = DataUtilFromTushare.load_daily_hists_v(symbols, '20190101', '20190115')
    print(quote)
    calendar = ts_pro.trade_cal(start_date='20100101', end_date='20210101', is_open=1)['cal_date'].to_list()
    print(calendar[::-1])
    df = ts_pro.adj_factor(ts_code='000001.SZ', trade_date='')
    print(df)

