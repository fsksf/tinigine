

from tinigine.interface import AbstractModule
from tinigine.utils.config import ConfigManager

mod_conf = ConfigManager(mod_name='data_from_tushare')


class DataFromTushare(AbstractModule):

    def set_up(self, env):
        self._env = env

    def tear_down(self):
        pass
