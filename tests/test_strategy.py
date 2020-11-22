# -*- coding:utf-8 -*-
"""
@author: ksf

@since: 2020/9/27 9:19 PM
"""


import pytest

from tinigine.core.engine import Engine
from tinigine.core.env import Environment
from tinigine.core.event_source import EventSource
from tinigine.core.params import Params
from tests.mock.mock_data_proxy import MockDataProxy


class TestStrategy:

    def setup(self):
        params = Params(algo_text='', algo_file=None, capital=10000000, start='20190102', end='20191101', freq='1d',
                        market='CN', currency='CNY')
        environment = Environment(params)
        event_source = EventSource(environment)
        environment.set_data_proxy(MockDataProxy())
        environment.set_event_source(event_source)
        engine = Engine(environment)
        self._engine = engine

    def teardown(self):
        pass

    def test_events(self):
        engine.run()




