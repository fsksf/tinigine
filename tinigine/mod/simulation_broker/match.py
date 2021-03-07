"""
@project: tinigine
@author: kang 
@github: https://github.com/fsksf 
@since: 2021/3/6 3:26 PM
"""
from tinigine.interface import AbstractEnv
from tinigine.core.order import Order
from tinigine.core.commission import CNStockCommission, Commission


class Matcher:
    def __init__(self, env: AbstractEnv):
        self._env = env
        self._broker = env.broker
        self._commission: Commission = None

    def set_commission(self, commission):
        self._commission = commission

    def market_order_cross(self, order: Order):
        reminder = order.quantity - order.filled_quantity
        current_price = self._env.data_proxy.current()
        price = current_price['close'][order.symbol]
        current_commission = self._commission.compute_commission(qty=reminder,
                                                                 price=price)