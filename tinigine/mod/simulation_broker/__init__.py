import click
from tinigine.__main__ import add_cmd
from tinigine.utils.config import ConfigManager
# for migrate
mod_conf = ConfigManager(mod_name='simulation_broker')


def load():
    from .mod import ModStandBroker
    mod_instance = ModStandBroker()
    return mod_instance




