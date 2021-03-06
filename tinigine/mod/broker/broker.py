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

class Broker(AbstractBroker):

    def __init__(self, env):
        self._env: AbstractEnv = env
        self._env.event_bus.add_event(self.on_order_submission, EventType.ORDER_SUBMISSION)
        self._order_manager = OrderManager(self._env)
        self._portfolio_manager = PortfolioManager(self._env)

    def order(self, symbol, quantity, limit_price=None, order_type=OrderType.MKT):
        if quantity > 0:
            side = OrderSide.BUY
        else:
            side = OrderSide.SELL
            quantity = abs(quantity)
        dt = self._env.data_proxy.get_datetime()
        order_obj = Order(symbol=symbol, quantity=quantity, side=side, order_type=order_type,
                          quantity=quantity, limit_price=limit_price, order_time=dt)

        evt = Event(event_type=EventType.ORDER_SUBMISSION, order_obj=order_obj)
        self._env.event_bus.emit(evt)

    def on_order_submission(self, event: Event):
        order_obj = self._order_manager.add(event.order_obj)


    def get_order(self, order_id):
        return self._order_manager.get_order(order_id)

    def get_positions(self):
        self._portfolio_manager