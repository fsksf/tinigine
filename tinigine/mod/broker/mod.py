

from tinigine.interface import AbstractModule, AbstractEnv


class ModStandBroker(AbstractModule):

    def set_up(self, env):
        self._env: AbstractEnv = env
        pass

    def tear_down(self):
        pass
