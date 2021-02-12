import click
from tinigine.__main__ import add_cmd
from tinigine.utils.config import ConfigManager
# for migrate
mod_conf = ConfigManager(mod_name='mod_template')


def load():
    from .mod import ModTemplate
    mod_instance = ModTemplate()
    return mod_instance


@add_cmd
@click.help_option('-h', '--help')
@click.option('-m', '--market', default='CN', help='市场')
@click.option('-f', '--freq', default='all', help='要更新的数据， {daily: 1d, minute: 1m, all: all}')
@click.pass_context
def mt_command_template(ctx):
    """
    command template
    """
    pass



