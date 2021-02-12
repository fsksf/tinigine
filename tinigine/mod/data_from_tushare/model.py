"""
@author: kang
@github: https://github.com/fsksf
@since: 2021/2/1 10:12 PM
"""
from sqlalchemy import Column, FLOAT, INT, VARCHAR, DATE, Index, BigInteger
from tinigine.utils.db import Base


class StockBasic(Base):
    """
    股票标的信息表
    """
    __tablename__ = 'stock_basic'
    id = Column(type_=BigInteger, primary_key=True)
    symbol = Column(type_=VARCHAR(20))
    name = Column(type_=VARCHAR(20))
    fullname = Column(type_=VARCHAR(50), doc='股票全称')
    area = Column(type_=VARCHAR(20), doc='所属地区')
    industry = Column(type_=VARCHAR(20), doc='所属行业')
    enname = Column(type_=VARCHAR(20), doc='英文名称')
    market = Column(type_=VARCHAR(20), doc='市场')
    exchange = Column(type_=VARCHAR(20), doc='交易所')
    currency = Column(type_=VARCHAR(10), doc='币种')
    list_status = Column(type_=VARCHAR(4), doc='上市状态')
    list_date = Column(INT, doc='上市时间')
    board = Column(type_=VARCHAR(10), doc='板块')
    delist_date = Column(INT, doc='退市时间')


Index("stock_basic_symbol_ix", StockBasic.symbol, unique=True)


class QuoteDaily(Base):
    __tablename__ = 'stock_quote_daily'
    id = Column(type_=BigInteger, primary_key=True)
    symbol = Column(name='symbol', type_=VARCHAR(20))
    timestamp = Column(type_=INT, doc='时间')
    open = Column(name='open', type_=FLOAT)
    high = Column(name='high', type_=FLOAT)
    low = Column(name='low', type_=FLOAT)
    close = Column(name='close', type_=FLOAT)
    volume = Column(type_=FLOAT, doc='成交量')


Index('stock_quote_daily_symbol_timestamp_ix', QuoteDaily.symbol, QuoteDaily.timestamp, unique=True)


class QuoteAdjFactors(Base):
    __tablename__ = 'stock_adj_factor'
    id = Column(type_=BigInteger, primary_key=True)
    symbol = Column(type_=VARCHAR(20))
    timestamp = Column(type_=INT, doc='时间')
    adj_factor = Column(type_=FLOAT, doc='复权因子')


Index('stock_adj_factor_symbol_timestamp_ix', QuoteAdjFactors.symbol, QuoteAdjFactors.timestamp, unique=True)


class DailyTradeCalender(Base):
    __tablename__ = 'daily_trade_calender'
    id = Column(type_=BigInteger, primary_key=True)
    market = Column(type_=VARCHAR(10), doc='市场')
    timestamp = Column(type_=INT, doc='交易日')
