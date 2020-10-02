# -*- coding:utf-8 -*-
"""
@author: ksf

@since: 2020/9/18 5:46 PM
"""

import os
import shutil
import yaml

from .utils import ensure_directory, merge_dict
from .logger import sys_logger

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))
MOD_PATH = os.path.join(ROOT_PATH, 'mod')


class ConfigManager:
    DEFAULT_CONFIG_FILE_NAME = 'config.system.yml'
    CONFIG_FILE_NAME = 'config.{mod}.yml'
    TINIGINE_PATH = 'TINIGINE_PATH'

    def __init__(self, user_config_path=None, mod_name='system'):
        self._mod_name = mod_name
        mod_dir = self.get_mod_default_dir(mod_name)
        self._default_config_path = os.path.join(mod_dir, self.DEFAULT_CONFIG_FILE_NAME)
        self._custom_dir = user_config_path or self.get_default_custom_dir()
        self._custom_config_path = self.get_custom_config_path()
        self._config_obj = self.merge_all()

    @staticmethod
    def get_mod_default_dir(mod_name):
        if mod_name == 'system':
            return ROOT_PATH
        return os.path.join(MOD_PATH, mod_name)

    def get_config(self):
        return self._config_obj

    def merge_all(self):
        """
        合并所有config
        :return:
        """
        default_config_obj = self.read_yml(self._default_config_path)
        custom_config_obj = self.read_yml(self._custom_config_path)
        return merge_dict(default_config_obj, custom_config_obj)

    @staticmethod
    def read_yml(self, file_path):
        with open(file_path, 'r') as f:
            config_obj = yaml.safe_load(f)
            return config_obj

    def get_custom_config_path(self, custom_dir=None):
        custom_dir = custom_dir or self.get_default_custom_dir()
        custom_config_dir = os.path.join(custom_dir, 'config')
        ensure_directory(custom_config_dir)
        return os.path.join(custom_config_dir, self.CONFIG_FILE_NAME.format(mod=self._mod_name))

    @classmethod
    def get_default_custom_dir(cls):
        """
        用户配置目录. 用于放置数据和配置
        """
        custom_dir = os.environ.get(cls.TINIGINE_PATH, None)
        if custom_dir is None:
            custom_dir = os.path.expanduser('~/.tinigine')
        ensure_directory(custom_dir)
        return custom_dir

    def generate_config_file(self, directory=None):
        """
        生成配置文件
        :param directory: 配置文件保存的目录. 若为 None 则保存在默认位置
        :return: 生成的配置文件路径
        """
        if not directory:
            directory = self.get_default_custom_dir()
        ensure_directory(directory)
        shutil.copy(self._default_config_path, self._custom_config_path)
        sys_logger.info(f"generate config file: {self._custom_config_path}")
        return self._custom_config_path
