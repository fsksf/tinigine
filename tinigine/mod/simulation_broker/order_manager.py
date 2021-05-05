"""
@project: tinigine
@author: kang 
@github: https://github.com/fsksf 
@since: 2021/3/4 6:44 PM
"""
from collections import defaultdict
from tinigine.interface import AbstractEnv
from tinigine.core.order import Order
from tinigine.core.constant import OrderStatus
from tinigine.core.event import EventType, Event
from tinigine.utils.info import OrderReason


class OrderManager:
    def __init__(self, env):
        self._env: AbstractEnv = env
        self._orders = []                                       # all orders
        self._open_orders = dict()                              # 未完成买卖轮回的浮动盈亏 orders
        self._pre_bar_orders = []                               # 上个bar下的单，当前bar 成交
        self._env.event_bus.add_event(self.on_order_submission_passed, EventType.ORDER_SUBMISSION_PASSED)
        self._env.event_bus.add_event(self.on_order_cancellation, EventType.ORDER_CANCELLATION)

    def add(self, order: Order):
        order_id = len(self._orders)
        order.set_order_id(order_id)
        self._orders.append(order)
        self._pre_bar_orders.append(order)
        return order

    def on_order_submission(self, order_obj):
        symbol = order_obj.symbol
        if self._open_orders.get(symbol, None) is not None:
            return OrderReason(result=False, reason='重复下单')
        return OrderReason(result=True, reason=None)

    def get_order(self, order_id):
        return self._orders[order_id]

    def get_orders(self):
        return self._orders.copy()

    def get_pre_orders(self):
        return self._pre_bar_orders.copy()

    def reset_pre_orders(self):
        self._pre_bar_orders = list()

    def on_order_submission_passed(self):
        for order in self._open_orders.values():
            if order.state == OrderStatus.NEW:
                order.state = OrderStatus.SUBMITTED
            self._env.broker.on_order_submission()

    def on_order_cancellation(self, event):
        order = event.order_obj
        state = order.state
        if state in (OrderStatus.NEW, OrderStatus.SUBMITTED, OrderStatus.PARTIALLY_FILLED):
            order.state = OrderStatus.CANCELLED
            self._env.broker.on_cancel_order(order.order_id)
            self._order_cancel_passed(order)
        elif state == OrderStatus.FILLED:
            order.info = 'The current order has been filled, so it cannot be cancelled.'
            self._order_cancel_rejected(order)

    def _order_cancel_passed(self, order):
        self._open_orders[order.symbol].remove(order)
        self._env.event_bus.emit(Event(EventType.ORDER_CANCELLATION_PASSED, order=order))

    def _order_cancel_rejected(self, order):
        self._env.event_bus.emit(Event(EventType.ORDER_CANCELLATION_REJECTED, order=order))

    def on_order_deal(self, order):
        pass

    def clean_open_orders(self):
        self._open_orders = dict()
