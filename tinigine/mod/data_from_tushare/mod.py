
from tinigine.__main__ import add_cmd
from tinigine.interface import AbstractModule, AbstractEnv
from .data_proxy import MysqlDataProxy


class DataFromTushare(AbstractModule):

    def set_up(self, env):
        self._env: AbstractEnv = env
        data_proxy = MysqlDataProxy(env=self._env)
        self._env.set_data_proxy(data_proxy)
        add_cmd(self._env.data_proxy.update_data)


    def tear_down(self):
        pass
