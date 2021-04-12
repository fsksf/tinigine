# -*- coding:utf-8 -*-
"""
@author: ksf

@since: 2020/9/18 6:07 PM
"""
import os
from importlib import import_module, reload
from errno import EEXIST
from functools import wraps
import tinigine.api
import tinigine.inner_api
import tinigine.core.event_bus
from tinigine.utils.local_instance import get_instance
from tinigine.utils.local_instance import InstanceApiDecorator

instance_api_decorator = InstanceApiDecorator


def ensure_directory(path):
    """
    检查并新建目录
    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == EEXIST and os.path.isdir(path):
            return
        raise


def merge_dict(this, other):
    """
    merge dict, 非dict的value会被后面的覆盖
    :param this: merge into
    :param other: merge from
    :return:
    """
    if not other:
        return this
    for key, value in other.items():
        if isinstance(value, dict):
            # get node or create one
            node = this.setdefault(key, {})
            merge_dict(node, value)
        else:
            this[key] = value
    return this


def local_method(instance_name='Strategy'):
    def outer_wp(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            algo_instance = get_instance(name=instance_name)
            return getattr(algo_instance, f.__name__)(*args, **kwargs)
        setattr(tinigine.api, f.__name__, wrapped)
        tinigine.api.__all__.append(f.__name__)
        f.is_api_method = True
        return f
    return outer_wp


def add_api_method(func):
    """
    添加func到用户环境
    :param func:
    :return:
    """
    def wrapped(*args, **kwargs):
        return func(*args, **kwargs)

    tinigine.api.__all__.append(func.__name__)
    setattr(tinigine.api, func.__name__, wrapped)
    wrapped.is_api_method = True
    return wrapped


def add_inner_api(func):
    """
    添加func到用户环境
    :param func:
    :return:
    """
    def wrapped(*args, **kwargs):
        return func(*args, **kwargs)

    tinigine.inner_api.__all__.append(func.__name__)
    setattr(tinigine.inner_api, func.__name__, wrapped)
    return wrapped


def import_inner_api(name):
    obj = import_module(name=name, package='tinigine.inner_api')
    return obj
