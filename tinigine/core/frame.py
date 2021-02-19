# -*- coding:utf-8 -*-
"""
@author: ksf

@since: 2020/8/27 8:24 AM
"""
import numpy as np
import pandas as pd

from .calender import Calender

class Frame:

    """
    Frame数据结构
    """

    def __init__(self, arr, index, name, columns):
        self._arr = arr
        self._index = Calender(None, index)
        self._name = name
        self._columns = columns

    @property
    def columns(self):
        return self._columns

    @property
    def name(self):
        return self._name

    @property
    def index(self):
        return self._index

    @property
    def arr(self):
        return self._arr

    def to_dataframe(self):
        data = pd.DataFrame(self.arr, index=self.index.cal_list, columns=self.columns)
        return data

    def append(self, other):
        raise NotImplementedError

    def ix(self, index):
        return dict(zip(self.columns, self.arr[index]))

    def i_of(self, ):
        pass

    def roll_calc(self, window, func):
        pass


class SFrame:

    def __init__(self, frame_dict=None):
        self.frame_dict = frame_dict if frame_dict else {}
        self.index: Calender = None
        self.columns = None

    def append(self, other):
        for frame in other.frame_dict.values():
            self.add(frame)

    def add(self, other: Frame):
        if (self.index is not None) and (self.columns is not None):
            if (other.index != self.index) or (other.columns != self.columns):
                raise ValueError('frame object mast be same index and columns')
        else:
            self.index = other.index
            self.columns = other.columns
        self.frame_dict[other.name] = other

    def to_dataframe(self):
        if not self.frame_dict:
            return pd.DataFrame()

        field_sr_list = []
        for field_name, frame in self.frame_dict.items():
            df = frame.to_dataframe()
            sr = df.stack()
            sr.name = field_name
            field_sr_list.append(sr)

        all_arr = pd.concat(field_sr_list, axis=1)
        return all_arr

    def history(self, start_id, before_bar_count):
        end_id = start_id + 1
        start_id = self.offset(end_id, before_bar_count)

        if not self.frame_dict:
            return pd.DataFrame()
        out = SFrame()
        for field_name, frame in self.frame_dict.items():
            out.add(Frame(arr=frame.arr[start_id: end_id], index=frame.index.cal_list[start_id: end_id], columns=frame.columns,
                          name=field_name))
        return out

    def offset(self, current_id, count):
        out_id = current_id - count
        return out_id

    def roll_calc(self, window, func):
        """
        进行滚动计算
        :param window:
        :param func:
        :return:
        """
        pass

    def ix(self, index):
        out = {}
        for frm in self.frame_dict.values():
            out[frm.name] = frm.ix(index)
        return out

    def i_of(self, o, side='gte'):
        if len(self.index) == 0:
            raise ValueError
        if side == 'gte':
            if o > self.index.o_of(-1):
                raise ValueError(f'{o} is grate than index max')
            try:
                return self.index.i_of(o)
            except KeyError:
                o += 1
                return self.i_of(o, side)
        elif side == 'lte':
            if o < self.index.o_of(0):
                raise ValueError(f'{o} is grate than index max')
            try:
                return self.index.i_of(o)
            except KeyError:
                o -= 1
                return self.i_of(o, side)
        return None

    def __len__(self):
        return len(self.index)
