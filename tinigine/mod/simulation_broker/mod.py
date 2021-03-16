

from tinigine.interface import AbstractModule, AbstractEnv
from .broker import Broker
from .event_source import EventSource


class ModStandBroker(AbstractModule):

    def set_up(self, env):
        self._env: AbstractEnv = env
        broker = Broker(self._env)
        event_source = EventSource(self._env)
        self._env.set_event_source(event_source)
        self._env.set_broker(broker)

    def tear_down(self):
        pass
