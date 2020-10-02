# -*- coding:utf-8 -*-
"""
@author: ksf

@since: 2020/9/21 8:27 PM
"""

from .frame import SFrame, Frame


class DataWalker:
    def __init__(self, sf: SFrame, start_time):
        self._sf = sf
        self._start_time = start_time
        self._index = self.get_index(start_time)
        self._end_index = len(self._sf)

    def current(self):
        return self._sf.ix(self._index)

    def get_index(self, _time):
        return self._sf.i_of(_time)

    def __index__(self):
        self._index += 1
        if self._index >= self._end_index:
            raise StopIteration
        return self
