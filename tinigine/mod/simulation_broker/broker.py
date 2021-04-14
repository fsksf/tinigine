"""
@project: tinigine
@author: kang 
@github: https://github.com/fsksf 
@since: 2021/3/2 8:37 AM
"""
from tinigine.core.constant import OrderType, OrderSide
from tinigine.core.order import Order
from tinigine.core.event import Event, EventType
from tinigine.interface import AbstractEnv, AbstractBroker
from .order_manager import OrderManager
from .portfolio_manager import PortfolioManager
from .match import Matcher


class Broker(AbstractBroker):

    def __init__(self, env):
        self._env: AbstractEnv = env
        self._env.event_bus.on(EventType.ORDER_NEW)(self.on_new_order)
        self._env.event_bus.add_event(self.on_order_submission, EventType.ORDER_SUBMISSION)
        self._env.event_bus.add_event(self.on_cancel_order, EventType.ORDER_CANCELLATION)
        self._order_manager = OrderManager(self._env)
        self._portfolio_manager = PortfolioManager(self._env)
        self._matcher = Matcher(self._env)

    def order(self, symbol, quantity, limit_price=None, order_type=OrderType.MKT):
        if quantity > 0:
            side = OrderSide.BUY
        else:
            side = OrderSide.SELL
            quantity = abs(quantity)
        dt = self._env.data_proxy.get_datetime()
        order_obj = Order(symbol=symbol, quantity=quantity, side=side, order_type=order_type,
                          limit_price=limit_price, order_time=dt)

        evt = Event(event_type=EventType.ORDER_NEW, order_obj=order_obj)
        self._env.event_bus.emit(evt)

    def on_cancel_order(self, evt: Event):
        pass

    def on_order_reject(self, evt: Event):
        pass

    def on_new_order(self, event: Event):
        order_obj = self._order_manager.add(getattr(event, 'order_obj'))
        return order_obj

    def on_order_submission(self, evt: Event):
        oder_obj = getattr(evt, 'order_obj')
        order_reason = self._order_manager.on_order_submission(oder_obj)
        flag = order_reason.result
        # ====================== 下单前验证 =====================
        if flag:
            order_reason = self._portfolio_manager.on_order_submission(oder_obj)
            flag = order_reason.result
        # ====================== 验证结束 ======================
        if flag:
            self._env.event_bus.emit()
        else:
            self._env.event_bus.emit(Event(event_type=EventType.ORDER_REJECTED, info=order_reason.reason))

    def get_order(self, order_id):
        return self._order_manager.get_order(order_id)

    def get_positions(self):
        self._portfolio_manager.get_positions()

    def get_orders(self):
        return self._order_manager.get_orders()

    def deal_order(self):
        self._matcher.limit_order_cross()
