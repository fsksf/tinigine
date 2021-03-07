"""
@project: tinigine
@author: kang 
@github: https://github.com/fsksf 
@since: 2021/2/3 11:10 PM
"""
from abc import ABC
import datetime
import sqlalchemy.exc as sqlexc
import pandas as pd
from tinigine.utils.db import DBConnect, DBUtil
from tinigine.core.event import EventType, Event
from tinigine.utils.datetime_utils import day_count
from tinigine.core.frame import Frame, SFrame
from tinigine.core.data_walker import DataWalker

from tinigine.interface import AbstractDataProxy
from .model import DailyTradeCalender, StockBasic, QuoteDaily, QuoteAdjFactors
from .downloader import DataUtilFromTushare
from tinigine.mod.data_from_tushare import mod_conf


class MysqlDataProxy(AbstractDataProxy, ABC):
    def __init__(self, env):
        super(MysqlDataProxy, self).__init__(env)
        # 订阅行情function 关联 订阅 事件
        self._env.event_bus.on(EventType.SUBSCRIBE)(self.on_subscribe)
        self._data_walker: DataWalker = None

    def get_sf(self):
        return self._cache

    @property
    def data_walker(self):
        return self._data_walker

    def get_calendar(self, start=None, end=None):
        with DBConnect() as s:
            data = s.query(DailyTradeCalender.timestamp).filter(
                DailyTradeCalender.market == self._env.params.market.name
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
        symbols_info_list = self.get_contract_info(symbols=None, market=str(self._env.params.market.name))
        return [d.symbol for d in symbols_info_list]

    @staticmethod
    def get_calender(start, end):
        cal_filter_list = [DailyTradeCalender.timestamp >= start]
        if end:
            cal_filter_list.append(DailyTradeCalender.timestamp <= end)
        cal_list = DBUtil.select([DailyTradeCalender.timestamp], filter_list=cal_filter_list)
        cal_list = pd.DataFrame(cal_list)['timestamp'].sort_values().to_list()
        return cal_list

    @staticmethod
    def get_quote(symbols, start, end):
        filter_list = [QuoteDaily.symbol.in_(symbols), QuoteDaily.timestamp >= start]
        if end:
            filter_list.append(QuoteDaily.timestamp <= end)
        daily = DBUtil.select([QuoteDaily], filter_list=filter_list)
        quote_no_br = pd.DataFrame(data=daily)
        del quote_no_br['id']
        return quote_no_br

    @staticmethod
    def get_factor(symbols, start, end):
        factor_filter_list = [QuoteAdjFactors.symbol.in_(symbols), QuoteAdjFactors.timestamp >= start]
        if end:
            factor_filter_list.append(QuoteAdjFactors.timestamp <= end)
        factor = DBUtil.select([QuoteAdjFactors], filter_list=factor_filter_list)
        factor_df = pd.DataFrame(factor)
        del factor_df['id']
        return factor_df

    def get_quote_br(self, symbols, start, end):
        quote_no_br = self.get_quote(symbols, start, end)
        factor_df = self.get_factor(symbols, start, end)
        cal_list = self.get_calendar(start, end)
        factor_df.set_index(['timestamp', 'symbol'], inplace=True)
        quote_no_br.set_index(['timestamp', 'symbol'], inplace=True)
        factor_df = factor_df['adj_factor'].unstack()
        factor_df = factor_df.reindex(cal_list, method='pad').reindex(symbols, axis=1)
        factor_df.fillna(value=1, inplace=True)
        factor_df = factor_df / factor_df.iloc[-1]
        sf = SFrame()
        for field in quote_no_br.columns:
            field_df = quote_no_br[field].unstack().reindex(cal_list)
            field_df = field_df.reindex(symbols, axis=1)
            if field == 'volume':
                field_df = field_df / factor_df
            else:
                field_df = field_df * factor_df
            fr = Frame(arr=field_df.to_numpy(), index=cal_list, columns=symbols, name=field)
            sf.add(fr)
        return sf

    def on_subscribe(self, event):
        symbols = event.symbols
        start = self._env.params.start
        end = self._env.params.end
        sf = self.get_quote_br(symbols, start, end)
        self._cache = sf
        self._data_walker = DataWalker(sf, start)

    def subscribe(self, symbols, before_bar_count=1):
        if isinstance(symbols, str):
            symbols = [symbols, ]
        evt = Event(event_type=EventType.SUBSCRIBE, symbols=symbols, before_bar_count=before_bar_count)
        self._env.event_bus.emit(event=evt)

    def dft_data_update(self):
        """
        data_from_tushare: 初始化、更新数据
        """
        symbols = self.download_symbols()
        start, end = self.download_calender()
        self.download_quote(symbols, start, end)
        # start, end = 20100101, 20210305
        self.download_factors(symbols, start=start, end=end)

    def download_symbols(self):
        new_basic = DataUtilFromTushare.load_basic(self._env.params.market)
        del new_basic['code']
        DBUtil.upsert(StockBasic, new_basic.to_dict(orient='records'), unique=[StockBasic.symbol, ])
        return self.get_symbols()

    def download_calender(self):
        params = self._env.params
        start_date = params.start
        end_date = params.end
        if end_date is None:
            params.end = end_date = datetime.datetime.today().strftime('%Y%m%d')
        last_sync_date = self.get_calendar()
        if last_sync_date:
            start_date = last_sync_date[-1] - 7
        calendar = DataUtilFromTushare.load_calendar(start_date=start_date, end_date=end_date)
        calendar = [{'market': str(params.market.name), 'timestamp': c} for c in calendar]
        for cal in calendar:
            try:
                DBUtil.insert(DailyTradeCalender, [cal])
            except sqlexc.IntegrityError:
                pass
        return start_date, end_date

    def download_quote(self, symbols, start, end):
        self._env.logger.info(f'download quote from {start} to {end}')
        calendar = self.get_calendar(start, end)
        count = 0
        total = len(calendar)

        for c in calendar:
            count += 1
            data = DataUtilFromTushare.load_daily_hists_h(trade_dates=[c], market=self._env.params.market)
            data.rename(columns={'trade_date': 'timestamp', 'vol': 'volume'}, inplace=True)
            data = data.to_dict(orient='records')
            self._env.logger.info(f'download quote from tushare date: {c}, progress: {count}/{total}')
            DBUtil.upsert(QuoteDaily, data, unique=[QuoteDaily.symbol, QuoteDaily.timestamp])

    def download_factors(self, symbols, start, end):
        total = len(symbols)
        day_count_len = day_count(start, end)
        step_len = total // day_count_len
        fetch_count = total // step_len + 1
        self._env.logger.info(f'download adj factors from {start} to {end} with symbols count {total}, step: {step_len}')
        for i in range(0, total, step_len):
            symbol = symbols[i:i+step_len]
            self._env.logger.info(f'download adj factors from tushare, progress: {i}/{total}')
            data = DataUtilFromTushare.load_adj_factors(symbols=symbol, start_date=start, end_date=end)
            data = data.to_dict(orient='records')
            DBUtil.upsert(QuoteAdjFactors, data, unique=[QuoteAdjFactors.symbol, QuoteAdjFactors.timestamp])
