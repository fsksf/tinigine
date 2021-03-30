"""
@project: tinigine
@author: kang 
@github: https://github.com/fsksf 
@since: 2021/3/16 8:13 PM
"""
from tinigine.core.constant import OrderType, OrderSide
from tests.base import BaseFixtureClass


class TestSimulationBroker(BaseFixtureClass):

    def test_order(self):
        self._env.broker.order('000001.SZ', quantity=100, order_type=OrderType.MKT)
        self._env.event_source.data_events()
        self._env.event_source.data_events()
        orders = self._env.broker.get_orders()
        assert len(orders) == 1

    def test_cancel_order(self):
        pass

    def test_get_orders(self):
        pass

    def test_get_positions(self):
        pass

