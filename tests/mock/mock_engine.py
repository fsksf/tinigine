# -*- coding:utf-8 -*-
"""
@author: ksf

@since: 2020/9/14 9:55 PM
"""
import os
from tinigine.core.env import Environment
from tinigine.core.engine import Engine
from tinigine.core.params import Params
from tinigine.utils.config import ConfigManager
from tinigine.core.constant import Freq
from .mock_data_proxy import MockDataProxy
from tests import TESTS_DIR

MOCK_TINIGINE_PATH = os.path.join(TESTS_DIR, '.tinigine')

os.environ[ConfigManager.TINIGINE_PATH] = MOCK_TINIGINE_PATH

params = Params(algo_text='', algo_file=None, capital=10000000, start='20190102', end='20191101', freq='1d',
                market='CN', currency='CNY')

environment = Environment(params)
environment.set_data_proxy(MockDataProxy())

engine = Engine(environment)
