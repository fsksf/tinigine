# -*- coding:utf-8 -*-
"""
@author: ksf

@since: 2020-04-25 21:29
"""

from enum import Enum


class Freq(Enum):
    MINUTE = '1m'
    DAILY = '1d'


class ContractType(Enum):

    STK = 'STK'
    FUT = 'FUT'
    OPT = 'OPT'


class OrderType(Enum):
    LMT = 'LMT'
    MKT = 'MKT'


class OrderSide(Enum):
    BUY = 'BUY'
    SELL = 'SELL'


class OrderStatus(Enum):
    NEW = 'NEW'                                 # 初始状态
    SUBMITTED = 'SUBMITTED'                     # 已经提交
    PARTIALLY_FILLED = 'PARTIALLY_FILLED'       # 部分成交
    FILLED = 'FILLED'                           # 全部成交
    PENDING_CANCEL = 'PENDING_CANCEL'           # 待取消
    CANCELLED = 'CANCELLED'                     # 已取消
    REJECTED = 'REJECTED'                       # 已拒绝


class Currency(Enum):
    USD = 'USD'
    HKD = 'HKD'
    CNH = 'CNH'
    CNY = 'CNY'


class Market(Enum):
    CN = 'CN'
    HK = 'HK'
    US = 'US'


FREQ_FORMAT_DICT = {
    Freq.DAILY: '%Y-%m-%d',
    Freq.MINUTE: '%Y-%m-%d %H:%M:%S'
}

HAND_LIMIT_COUNT = {
    Market.CN: 100
}