"""
@project: tinigine
@author: kang 
@github: https://github.com/fsksf 
@since: 2021/2/3 9:12 PM
"""

from tinigine.core.engine import Engine
from tinigine.core.env import Environment
from tinigine.core.params import Params


def mock_env():
    params = Params()
    env = Environment(params)
    Engine(env).load_mod()
