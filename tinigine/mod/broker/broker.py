"""
@project: tinigine
@author: kang 
@github: https://github.com/fsksf 
@since: 2021/3/2 8:37 AM
"""
from tinigine.core.constant import OrderType, OrderSide
from tinigine.core.order import Order
from tinigine.core.event import Event, EventType
from tinigine.interface import AbstractEnv


class Broker:

    def __init__(self, env):
        self._env: AbstractEnv = env

    def order(self, symbol, quantity, limit_price=None, type_=OrderType.MKT):
        if quantity > 0:
            side = OrderSide.BUY
        else:
            side = OrderSide.SELL
            quantity = abs(quantity)
        order_obj = Order(symbol=symbol, quantity=quantity, side=side,
                          quantity=quantity, limit_price=limit_price, type)

        evt = Event(event_type=EventType.ORDER_NEW, order_obj=order_obj)
        self._env.event_bus.emit(evt)