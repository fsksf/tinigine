"""
@project: tinigine
@author: kang 
@github: https://github.com/fsksf 
@since: 2021/3/4 6:44 PM
"""
from tinigine.interface import AbstractEnv
from tinigine.utils.info import OrderReason

class PortfolioManager:
    def __init__(self, env: AbstractEnv):
        self._env: AbstractEnv = env

    def get_positions(self):
        pass

    def on_order_submission(self, order):

        return OrderReason(result=True, reason=None)