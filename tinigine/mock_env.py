"""
@project: tinigine
@author: kang 
@github: https://github.com/fsksf 
@since: 2021/2/3 9:12 PM
"""

from tinigine.core.engine import Engine
from tinigine.core.env import Environment
from tinigine.core.params import Params
from tinigine.config import conf

def mock_env():
    p_config = conf.get_config()['params']
    params = Params(**p_config)
    env = Environment(params)
    Engine(env).load_mod()
