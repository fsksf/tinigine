"""
@project: tinigine
@author: kang 
@github: https://github.com/fsksf 
@since: 2021/3/6 8:14 AM
"""

import pytest

from tinigine.core.engine import Engine
from tinigine.core.env import Environment
from tinigine.core.event_source import EventSource
from tinigine.core.params import Params
from tests.mock.mock_mysql_data_proxy import MockMysqlDataProxy

strategy_str = """
from tinigine.api import *

def initialize(context):
    print(context)
    subscribe(['000001.SZ'], 10)

def on_bar(context, data):
    print(context)
    print(data.current())
    print(data.history(5).to_dataframe())

"""


class TestEngine:

    def setup(self):
        params = Params(algo_text=strategy_str, algo_file=None, capital=10000000, start=20190102, end=20191101,
                        freq='1d',
                        market='CN', currency='CNY')
        environment = Environment(params)
        environment.set_data_proxy(MockMysqlDataProxy(environment))
        event_source = EventSource(environment)
        environment.set_event_source(event_source)
        engine = Engine(environment)
        self._engine = engine

    def teardown(self):
        pass

    def test_events(self):
        self._engine.run()