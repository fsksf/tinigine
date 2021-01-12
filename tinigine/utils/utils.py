# -*- coding:utf-8 -*-
"""
@author: ksf

@since: 2020/9/18 6:07 PM
"""

from functools import wraps
import tinigine.api
import tinigine.core.event_bus
from tinigine.utils.local_instance import get_instance


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
    for key, value in other.items():
        if isinstance(value, dict):
            # get node or create one
            node = this.setdefault(key, {})
            merge_dict(node, value)
        else:
            this[key] = value
    return this


def api_method(instance_name='Strategy'):
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


def add_api(func):
    setattr(tinigine.api, func.__name__, func)
    tinigine.api.__all__.append(func.__name__)
    return func
