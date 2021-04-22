

from tinigine.interface import AbstractModule, AbstractEnv
from .broker import Broker


class ModStandBroker(AbstractModule):

    def set_up(self, env):
        self._env: AbstractEnv = env
        broker = Broker(self._env)
        self._env.set_broker(broker)

    def tear_down(self):
        pass
