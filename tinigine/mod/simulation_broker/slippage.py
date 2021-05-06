"""
@project: tinigine
@author: kang 
@github: https://github.com/fsksf 
@since: 2021/3/6 6:20 PM
"""
from tinigine.interface import Slippage
from tinigine.core.order import Order
from tinigine.core.constant import OrderSide
from tinigine.utils.utils import add_inner_api


@add_inner_api
class FixedSlippage(Slippage):
    def __init__(self, spread=0.0):
        self.spread = spread

    def process_order(self, order: Order, filling_price):
        if order.side == OrderSide.BUY:
            order.filled_price += self.spread
        else:
            order.filled_price -= self.spread
        # order.realized_pnl -= self.spread * order.filled

    def to_dict(self):
        return {'type': 'fix', 'spread': self.spread}


@add_inner_api
class FixedBasisPointsSlippage(Slippage):
    basis_points = 0
    volume_limit = 0.1

    @classmethod
    def process_order(cls, order: Order, filling_price):
        gap = filling_price * cls.basis_points
        if order.side == OrderSide.BUY:
            order.filled_price = filling_price + gap
        else:
            order.filled_price = filling_price - gap

    @classmethod
    def to_dict(cls):
        return {'type': 'fixbasis', 'basis_points': cls.basis_points, 'volume_limit': cls.volume_limit}
