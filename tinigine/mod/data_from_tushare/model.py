"""
@author: kang
@github: https://github.com/fsksf
@since: 2021/2/1 10:12 PM
"""
from sqlalchemy import Column, FLOAT, INT, VARCHAR
from tinigine.utils.db import Base


class StockBasic(Base):
    """
    股票标的信息表
    """
    __tablename__ = 'stock_basic'


class QuoteDaily(Base):
    __tablename__ = 'quote_daily'
    symbol = Column(name='symbol', type_=VARCHAR(20))
    open = Column(name='open', type_=FLOAT)
    high = Column(name='high', type_=FLOAT)
    low = Column(name='low', type_=FLOAT)
    close = Column(name='close', type_=FLOAT)