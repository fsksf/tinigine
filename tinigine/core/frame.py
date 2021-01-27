# -*- coding:utf-8 -*-
"""
@author: ksf

@since: 2020/8/27 8:24 AM
"""
import numpy as np
import pandas as pd


class Frame:

    """
    Frame数据结构
    """

    def __init__(self, arr, index, name, columns):
        self._arr = arr
        self._index = index
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
        data = pd.DataFrame(self.arr, index=self.index, columns=self.columns)
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
        self.index = None
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
        arr_list = []
        symbol_list = []
        for frame in self.frame_dict.values():
            arr_list.append(frame.arr)
            symbol_list.append(frame.symbol)

        index_obj = pd.MultiIndex.from_product([symbol_list, self.index], names=['symbol', 'timestamp']).swaplevel(0, 1)

        all_arr = np.concatenate(arr_list)

        data = pd.DataFrame(all_arr, index=index_obj, columns=self.columns)
        data.reset_index(inplace=True)
        return data

    def history(self, before_bar_count):
        pass

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
            if o > self.index[-1]:
                raise ValueError(f'{o} is grate than index max')
            for i, item in list(enumerate(self.index))[::-1]:
                if item < o:
                    return i+1
                elif item == o:
                    return i

        elif side == 'lte':
            if o < self.index[0]:
                raise ValueError(f'{o} is lt than index min')
            for i, item in list(enumerate(self.index))[::-1]:
                if item > o:
                    return i-1
                elif item == 0:
                    return i
        return None

    def __len__(self):
        return len(self.index)
