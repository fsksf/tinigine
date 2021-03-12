"""
@project: tinigine
@author: kang 
@github: https://github.com/fsksf 
@since: 2021/3/4 7:30 PM
"""
from tinigine.interface import AbstractEnv
from tinigine.core.constant import Currency, Market


class Portfolio:
    def __init__(self, env: AbstractEnv, available_funds=1000, currency=Currency.CNY, market=Market.CN):
        self._env: AbstractEnv = env
        self._available_funds = available_funds
        self._currency = currency
        self._market = market

    @property
    def position_value(self):
        current_price = self._env.data_proxy.data_walker.current()

    @property
    def total_assets(self):
        return self._available_funds + self.position_value
