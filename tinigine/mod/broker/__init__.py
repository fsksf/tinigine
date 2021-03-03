import click
from tinigine.__main__ import add_cmd
from tinigine.utils.config import ConfigManager
# for migrate
mod_conf = ConfigManager(mod_name='mod_stand_broker')


def load():
    from .mod import ModTemplate
    mod_instance = ModTemplate()
    return mod_instance




