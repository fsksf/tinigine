"""
@project: tinigine
@author: kang 
@github: https://github.com/fsksf 
@since: 2021/3/2 11:52 AM
"""

from .constant import OrderSide, OrderStatus, OrderType


class Order:

    def __init__(self, symbol, quantity, side=OrderSide.BUY, order_type=OrderType.MKT,
                 limit_price=None, order_time=None, trade_time=None,
                 filled_price=None, filled_quantity=0, state=OrderStatus.NEW,
                 commission=0):
        self.order_id = None
        self.symbol = symbol
        self.quantity = quantity
        self.side = side
        self.order_type = order_type
        self.limit_price = limit_price
        self.order_time = order_time
        self.trade_time = trade_time
        self.filled_price = filled_price
        self.filled_quantity = filled_quantity
        self.state = state
        self.commission = commission

    def to_dict(self):
        ret = {k: v for k,v in self.__dict__.items() if not str(k).startswith('_')}
        return ret

    def set_order_id(self, order_id):
        self.order_id = order_id

    def add_commission(self, commission):
        self.commission += commission
