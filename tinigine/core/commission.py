"""
@project: tinigine
@author: kang 
@github: https://github.com/fsksf 
@since: 2021/3/6 3:44 PM
"""


class Commission:
    @classmethod
    def compute_commission(cls, qty=0, price=0):
        raise NotImplementedError


class CNStockCommission(Commission):
    TRADE_COMMISSION_PCT = 0.00025
    TRADE_COMMISSION_LEAST = 5

    @classmethod
    def compute_commission(cls, qty=0, price=0):
        trade_commission_by_pct = qty * price * cls.TRADE_COMMISSION_PCT
        if trade_commission_by_pct > cls.TRADE_COMMISSION_LEAST:
            return trade_commission_by_pct
        else:
            return cls.TRADE_COMMISSION_LEAST


