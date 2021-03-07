"""
@project: tinigine
@author: kang 
@github: https://github.com/fsksf 
@since: 2021/3/6 6:20 PM
"""
from tinigine.core.constant import OrderSide


class Slippage:
    def process_order(self, order):
        pass

    def to_dict(self):
        pass


class FixedSlippage(Slippage):
    def __init__(self, spread=0.0):
        self.spread = spread

    def process_order(self, order):
        if order.side == OrderSide.BUY:
            order.filled_price += self.spread
        else:
            order.filled_price -= self.spread
        # order.realized_pnl -= self.spread * order.filled

    def to_dict(self):
        return {'type': 'fix', 'spread': self.spread}


class FixedBasisPointsSlippage(Slippage):
    def __init__(self, basis_points=0.0, volume_limit=1.0):
        self.basis_points = basis_points
        self.volume_limit = volume_limit

    def process_order(self, order):
        gap = order.quantity * self.basis_points
        if order.side == OrderSide.BUY:
            order.filled_price += gap
        else:
            order.filled_price -= gap
        # order.realized_pnl -= gap * order.filled

    def to_dict(self):
        return {'type': 'fixbasis', 'basis_points': self.basis_points, 'volume_limit': self.volume_limit}
