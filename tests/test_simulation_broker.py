"""
@project: tinigine
@author: kang 
@github: https://github.com/fsksf 
@since: 2021/3/16 8:13 PM
"""
import pytest

from tinigine.core.engine import Engine
from tinigine.core.env import Environment
from tinigine.core.event import Event, EventType
from tinigine.core.constant import OrderType, OrderSide
from tinigine.mod.simulation_broker.event_source import EventSource
from tinigine.core.params import Params
from tests.mock.mock_mysql_data_proxy import MockMysqlDataProxy
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

