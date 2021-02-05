"""
@project: tinigine
@author: kang 
@github: https://github.com/fsksf 
@since: 2021/2/3 11:03 PM
"""
from .data_util import DataUtilFromTushare


class DownloadFromTushare:

    @staticmethod
    def download_stock_basic(market='CN'):
        data = DataUtilFromTushare.load_basic(market)
        DataUtilFromTushare.load_calendar()

    def download_daily_quote(self):
        pass

    def download_trade_calender(self):
        pass