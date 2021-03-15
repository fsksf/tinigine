"""
@project: tinigine
@author: kang 
@github: https://github.com/fsksf 
@since: 2021/3/6 3:26 PM
"""
from tinigine.interface import AbstractEnv, Slippage
from tinigine.core.order import Order
from tinigine.core.commission import CNStockCommission, Commission
from tinigine.core.constant import HAND_LIMIT_COUNT
from tinigine.mod.simulation_broker import mod_conf
from tinigine.utils.utils import import_inner_api

slippage_class_name = mod_conf['FixedBasisPointsSlippage']
slippage_class: Slippage = import_inner_api(name=slippage_class_name)


class Matcher:
    def __init__(self, env: AbstractEnv):
        self._env = env
        self._broker = env.broker
        self._commission: Commission = None

    def set_commission(self, commission):
        self._commission = commission

    def market_order_cross(self, order: Order):
        reminder = order.quantity - order.filled_quantity
        hand_limit_count = HAND_LIMIT_COUNT[self._env.params.market]
        if reminder % hand_limit_count > 0.0:
            raise ValueError(f'quantity error: {order.to_dict()}')
        current_price = self._env.data_proxy.current()
        price = current_price['close'][order.symbol]
        hand_max_limit = (current_price['volume'] * mod_conf['trade_max_pct']) // 100 * 100
        if reminder > hand_max_limit:
            reminder = hand_max_limit
        current_commission = self._commission.compute_commission(qty=reminder,
                                                                 price=price)
        order.add_commission(current_commission)
        slippage_class.process_order(order=order, filling_price=price)

    def limit_order_cross(self, order):
        pass