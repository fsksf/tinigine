# -*- coding:utf-8 -*-
"""
@author: ksf

@since: 2020/9/21 8:27 PM
"""

from collections import Iterable
from .frame import SFrame, Frame


class DataWalker(Iterable):
    def __init__(self, sf: SFrame, start_time):
        self._sf = sf
        self._start_time = start_time
        self._index = self.get_index(start_time)
        self._end_index = len(self._sf)

    def current(self):
        return self._sf.ix(self._index)

    @property
    def current_index(self):
        return self._index

    @current_index.setter
    def set_current_index(self, value):
        self._index = value

    def history(self, before_bar_count):
        return self._sf.history(start_id=self._index + 1, before_bar_count=before_bar_count)

    def get_index(self, _time):
        return self._sf.i_of(_time)

    def __next__(self):
        self._index += 1
        if self._index >= self._end_index:
            raise StopIteration
        return self

    def __iter__(self):
        return self
