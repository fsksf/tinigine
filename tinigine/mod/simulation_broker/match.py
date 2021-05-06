"""
@project: tinigine
@author: kang 
@github: https://github.com/fsksf 
@since: 2021/3/6 3:26 PM
"""
from tinigine.interface import AbstractEnv, Slippage
from tinigine.core.order import Order
from tinigine.core.constant import OrderType, OrderSide, OrderStatus
from tinigine.mod.simulation_broker.commission import Commission
from tinigine.core.constant import HAND_LIMIT_COUNT
from tinigine.mod.simulation_broker import mod_conf
from tinigine.utils.utils import import_inner_api
from .slippage import FixedBasisPointsSlippage, FixedSlippage

slippage_class_name = mod_conf['slippage_class']
slippage_class: Slippage = import_inner_api(name=slippage_class_name)

commission_class_name = mod_conf['commission_class']
commission_class = import_inner_api(name=commission_class_name)


class Matcher:
    def __init__(self, env: AbstractEnv):
        self._env = env
        self._broker = env.broker
        self._commission: Commission = commission_class

    def set_commission(self, commission):
        self._commission = commission

    def order_cross(self, order: Order):
        if order.order_type == OrderType.LMT:
            return self.limit_order_cross(order)
        elif order.order_type == OrderType.MKT:
            return self.market_order_cross(order)
        raise NotImplementedError

    def market_order_cross(self, order: Order):
        reminder = self.check_quantity(order)
        current_price = self._env.data_proxy.current()
        price = current_price['open'][order.symbol]

        current_commission = self._commission.compute_commission(qty=reminder,
                                                                 price=price)
        order.add_commission(current_commission)
        slippage_class.process_order(order=order, filling_price=price)

    def limit_order_cross(self, order):
        current_price = self._env.data_proxy.current()
        price = current_price['open'][order.symbol]
        reminder = self.check_quantity(order)
        if order.side == OrderSide.BUY:
            if order.limit_price < price:
                order.state = OrderStatus.FAIL
                return order
        else:
            if order.limit_price > price:
                order.state = OrderStatus.FAIL
                return order

        current_commission = self._commission.compute_commission(qty=reminder,
                                                                 price=price)
        order.add_commission(current_commission)
        slippage_class.process_order(order=order, filling_price=price)

    def check_quantity(self, order: Order):
        reminder = order.quantity - order.filled_quantity
        current_price = self._env.data_proxy.current()
        hand_limit_count = HAND_LIMIT_COUNT[self._env.params.market]
        if reminder % hand_limit_count > 0.0:
            raise ValueError(f'quantity error: {order.to_dict()}')

        hand_max_limit = (current_price['volume'][order.symbol] * mod_conf['trade_max_pct']) // 100 * 100
        if reminder > hand_max_limit:
            reminder = hand_max_limit
        return reminder
