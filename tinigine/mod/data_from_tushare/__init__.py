import click
from tinigine.__main__ import add_cmd
from tinigine.utils.config import ConfigManager
# for migrate
from .model import *
mod_conf = ConfigManager(mod_name='data_from_tushare')


def load():
    from .mod import DataFromTushare
    mod_instance = DataFromTushare()
    return mod_instance


@add_cmd
@click.help_option('-h', '--help')
@click.option('-d', '--directory', type=click.Path(), default=None)
def dft_gen_config(directory):
    """
    data_from_tushare: 初始化config文件
    """
    mod_conf.generate_config_file(directory)

