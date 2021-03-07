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
    print(data.current())


"""


class TestEngine:

    def setup(self):
        params = Params(algo_text=strategy_str, algo_file=None, capital=10000000, start=20190102, end=20191101,
                        freq='1d',
                        market='CN', currency='CNY')
        environment = Environment(params)
        engine = Engine(environment)
        environment.set_data_proxy(MockMysqlDataProxy(environment))
        event_source = EventSource(environment)
        environment.set_event_source(event_source)
        self._env = environment
        self._engine = engine
        self._env.data_proxy.subscribe(['000001.SZ', '600600.SH'], before_bar_count=10)

    def teardown(self):
        pass

    def test_events(self):
        # self._engine.run()
        pass

    def test_symbols(self):
        symbols = self._env.data_proxy.get_symbols()
        assert symbols == ['000001.SZ', '600600.SH', '600703.SH']

    @pytest.mark.parametrize("start,end,result", [
        (20100101, 20200101, 20100104),
        (20180101, 20200101, 20180102)
    ])
    def test_calender(self, start, end, result):

        calender = self._env.data_proxy.get_calendar(start, end)
        assert calender[0] == result

    def test_subscribe(self):
        first_data = self._env.data_proxy.data_walker.current()
        assert first_data['close']['000001.SZ'] == 9.19

    def test_data_walker(self):
        data_walker = self._env.data_proxy.data_walker
        current = data_walker.current()
        assert current['open']['000001.SZ'] == 9.39
        history = data_walker.history(3)
        print(history.to_dataframe())