"""
@project: tinigine
@author: kang 
@github: https://github.com/fsksf 
@since: 2021/2/3 11:10 PM
"""
from abc import ABC
import click
from tinigine.__main__ import cli
from tinigine.utils.db import DBConnect, DBUtil

from tinigine.interface import AbstractDataProxy
from .model import DailyTradeCalender, StockBasic, QuoteDaily
from .downloader import DataUtilFromTushare
from tinigine.mod.data_from_tushare import mod_conf


class MysqlDataProxy(AbstractDataProxy, ABC):
    def __init__(self, env):
        super(MysqlDataProxy, self).__init__(env)

    def get_sf(self):
        pass

    def get_calendar(self, start=None, end=None):
        with DBConnect() as s:
            data = s.query(DailyTradeCalender.timestamp).filter(
                DailyTradeCalender.market == self._env.params.market
            )
            if start:
                data = data.filter(
                    DailyTradeCalender.timestamp >= start
                )
            if end:
                data = data.filter(
                    DailyTradeCalender.timestamp <= end
                )
        return [d[0] for d in data.all()]

    def _get_last(self):
        data = self.get_calendar()
        if data:
            return data[-1]
        else:
            return mod_conf[self._env.params.freq]['start']

    def get_contract_info(self, symbols=None, market=None, industry=None):
        with DBConnect() as s:
            data = s.query(StockBasic)
            if symbols:
                data = data.filter(StockBasic.symbol.in_(symbols))
            if market:
                data = data.filter(StockBasic.market == market)
            if industry:
                data = data.filter(StockBasic.industry == industry)
            data = data.all()
        return data

    def get_symbols(self):
        symbols_info_list = self.get_contract_info(symbols=None, market=str(self._env.params.market))
        return [d.symbol for d in symbols_info_list]

    def data_update(self):
        """
        初始化、更新数据
        """
        symbols = self.download_symbols()
        start, end = self.download_calender()
        self.download_quote(symbols, 20100104, 20211231)

    def download_symbols(self):
        new_basic = DataUtilFromTushare.load_basic(self._env.params.market)
        del new_basic['code']
        DBUtil.upsert(StockBasic, new_basic.to_dict(orient='records'), unique=[StockBasic.symbol, ])
        return self.get_symbols()

    def download_calender(self):
        params = self._env.params
        start_date = params.start
        end_date = params.end
        last_sync_date = self.get_calendar()
        if last_sync_date:
            start_date = last_sync_date[-1] + 1
        calendar = DataUtilFromTushare.load_calendar(start_date=start_date, end_date=end_date)
        calendar = [{'market': str(params.market), 'timestamp': c} for c in calendar]
        if calendar:
            DBUtil.insert(DailyTradeCalender, calendar)
        return start_date, end_date

    def download_quote(self, symbols, start, end):
        calendar = self.get_calendar(start, end)
        count = 0
        total = len(calendar)
        for c in calendar:
            count += 1
            data = DataUtilFromTushare.load_daily_hists_h(codes=symbols, trade_dates=[c], market=self._env.params.market)
            data.rename(columns={'trade_date': 'timestamp', 'vol': 'volume'}, inplace=True)
            data = data.to_dict(orient='records')
            self._env.logger.info(f'download quote from tushare date: {c}, progress: {count}/{total}')
            DBUtil.upsert(QuoteDaily, data, unique=[QuoteDaily.symbol, QuoteDaily.timestamp])