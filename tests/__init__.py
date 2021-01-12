# -*- coding:utf-8 -*-
"""
@author: ksf

@since: 2020/9/14 9:55 PM
"""
import os
from tinigine.utils.config import ConfigManager

TESTS_DIR = os.path.dirname(__file__)

MOCK_TINIGINE_PATH = os.path.join(TESTS_DIR, '.tinigine')

os.environ[ConfigManager.TINIGINE_PATH] = MOCK_TINIGINE_PATH