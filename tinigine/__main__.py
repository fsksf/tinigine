"""
@project: tinigine
@author: kang 
@github: https://github.com/fsksf 
@since: 2021/2/2 7:21 PM
"""
from tinigine import CMD_LIST
from tinigine.config import conf
from tinigine.core.engine import Engine
from tinigine.core.env import Environment
from tinigine.core.params import Params

import click


@click.group()
@click.help_option('-h', '--help')
@click.version_option(version=conf.get_version())
@click.pass_context
def cli(ctx):
    pass


@cli.command()
@click.help_option('-h', '--help')
@click.option('-d', '--directory', type=click.Path(), default=None)
def gen_config(directory):
    """
    生成配置文件
    """
    path = conf.generate_config_file(directory)
    print('Generate config file: %s' % path)


def add_cmd(func):
    CMD_LIST.append(func)
    return func


def entry():
    params = Params()
    env = Environment(params)
    Engine(env).load_mod()
    for cmd in CMD_LIST:
        cli.add_command(cmd)
    cli()


if __name__ == '__main__':
    entry()
