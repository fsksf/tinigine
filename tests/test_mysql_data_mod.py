"""
@project: tinigine
@author: kang 
@github: https://github.com/fsksf 
@since: 2021/3/6 8:14 AM
"""

import pytest
from tests.base import BaseFixtureClass

strategy_str = """
from tinigine.api import *

def initialize(context):
    print(context)
    subscribe(['000001.SZ'], 10)

def on_bar(context, data):
    print(data.current())


"""


class TestMysqlDataProxy(BaseFixtureClass):

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
        first_data = self._env.data_proxy.current()
        assert first_data['close']['000001.SZ'] == 9.19

    def test_get_datetime(self):
        dt = self._env.data_proxy.get_datetime()
        assert dt == 20190102

    def test_data_walker(self):
        data_walker = self._env.data_proxy.data_walker
        current = data_walker.current()
        assert current['open']['000001.SZ'] == 9.39
        history = data_walker.history(3)
        print(history.to_dataframe())
