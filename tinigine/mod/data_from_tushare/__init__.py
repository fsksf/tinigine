import click
from tinigine.__main__ import add_cmd
from tinigine.utils.config import ConfigManager

mod_conf = ConfigManager(mod_name='data_from_tushare')


def load():
    from .mod import DataFromTushare
    mod_instance = DataFromTushare()
    return mod_instance

@add_cmd
@click.command()
@click.help_option('-h', '--help')
@click.option('-m', '--market', default='CN', help='市场')
@click.option('-f', '--freq', default='all', help='要更新的数据， {daily: 1d, minute: 1m, all: all}')
@click.pass_context
def quote_init(ctx):
    pass


from tinigine import CMD_LIST
print('init command', CMD_LIST)
