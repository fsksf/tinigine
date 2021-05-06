"""
@project: tinigine
@author: kang 
@github: https://github.com/fsksf 
@since: 2021/5/6 8:05 PM
"""

import pytest

from tinigine.core.engine import Engine
from tinigine.core.env import Environment
from tinigine.core.params import Params
from tests.mock.mock_mysql_data_proxy import MockMysqlDataProxy


strategy_str = """
from tinigine.api import *
import tinigine.api as api
print(api)
print(dir(api))

def initialize(context):
    print(context)
    subscribe(['000001.SZ'], 10)

def on_bar(context, data):
    order('000001.SZ', 100)

"""


class TestMysqlDataProxy:

    def setup_method(self):
        params = Params(algo_text=strategy_str, algo_file=None, capital=10000000, start=20190102, end=20191101,
                        freq='1d',
                        market='CN', currency='CNY')
        environment = Environment(params)
        engine = Engine(environment)
        environment.set_data_proxy(MockMysqlDataProxy(environment))
        self._env = environment
        self._engine = engine
        self._env.data_proxy.subscribe(['000001.SZ', '600600.SH'], before_bar_count=10)

    def teardown_method(self):
        pass

    def test_order(self):
        self._engine.run()
