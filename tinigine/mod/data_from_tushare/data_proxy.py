"""
@project: tinigine
@author: kang 
@github: https://github.com/fsksf 
@since: 2021/2/3 11:10 PM
"""
from abc import ABC
import click
from tinigine.__main__ import cli
from tinigine.utils.db import DBConnect

from tinigine.interface import AbstractDataProxy
from .model import DailyTradeCalender, StockBasic
from .downloader import DataUtilFromTushare
from tinigine.mod.data_from_tushare import mod_conf


class MysqlDataProxy(AbstractDataProxy, ABC):

    def get_sf(self):
        pass

    def get_calendar(self):
        with DBSession() as s:
            data = s.query(DailyTradeCalender.timestamp).fliter(
                DailyTradeCalender.market == self._env.params.market
            ).all()
        return [d[0] for d in data]

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
        pass

    def update_data(self):
        """
        初始化、更新数据
        """
        self.download_symbols()

    def download_symbols(self):
        new_basic = DataUtilFromTushare.load_basic(self._env.params.market)
        old_basic = self.get_contract_info()

        with DBConnect() as s
            del new_basic['code']
            s.add_all([StockBasic(**kw) for kw in new_basic.to_dict(orient='record')])
            s.commit()