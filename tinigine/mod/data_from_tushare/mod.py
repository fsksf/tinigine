
from tinigine.interface import AbstractModule


class DataFromTushare(AbstractModule):

    def set_up(self, env):
        self._env = env

    def tear_down(self):
        pass
