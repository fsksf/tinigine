"""
@project: tinigine
@author: kang 
@github: https://github.com/fsksf 
@since: 2021/3/4 6:44 PM
"""
from tinigine.interface import AbstractEnv


class PortfolioManager:
    def __init__(self, env: AbstractEnv):
        self._env: AbstractEnv = env

    def get_positions(self):
        pass
