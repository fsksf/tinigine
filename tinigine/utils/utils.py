# -*- coding:utf-8 -*-
"""
@author: ksf

@since: 2020/9/18 6:07 PM
"""


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
