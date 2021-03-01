# -*- coding:utf-8 -*-
"""
@author: ksf

@since: 2020-04-25 21:21
"""

from tinigine.core.engine import Engine
from tinigine.core.env import Environment
from tinigine.core.params import Params
from tinigine.config import conf

strategy_str = """
from tinigine.api import *

def initialize(context):
    print(context)
    subscribe('000001.SZ', 10)

def on_bar(context, data):
    print(context)
    print(data.current())
    print(data.history(5).to_dataframe())

"""


def main():
    p_config = conf.get_config()['params']
    params = Params(**p_config)
    params.set_algo(strategy_str)
    env = Environment(params)
    engine = Engine(env)
    engine.run()


if __name__ == '__main__':
    main()