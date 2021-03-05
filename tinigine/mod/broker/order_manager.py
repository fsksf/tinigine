"""
@project: tinigine
@author: kang 
@github: https://github.com/fsksf 
@since: 2021/3/4 6:44 PM
"""
from collections import defaultdict
from tinigine.interface import AbstractEnv
from tinigine.core.order import Order


class OrderManager:
    def __init__(self, env):
        self._env: AbstractEnv = env
        self._orders = []
        self._symbol_orders = defaultdict(list)

    def add(self, order: Order):
        order_id = len(self._orders)
        order.set_order_id(order_id)
        return order

    def get_order(self, order_id):
        return self._orders[order_id]