"""
@project: tinigine
@author: kang 
@github: https://github.com/fsksf 
@since: 2021/2/19 6:55 PM
"""


class Calender:

    def __init__(self, freq, cal_list):
        self._cal_i_map = {c: i for c, i in zip(cal_list, range(len(cal_list)))}
        self._cal_list = cal_list

    def i_of(self, dt):
        return self._cal_i_map[dt]

    def o_of(self, i):
        return self._cal_list[i]

    @property
    def cal_list(self):
        return self._cal_list

    def is_month_start(self, dt):
        current_i = self.i_of(dt)
        pre_i = current_i - 1
        if pre_i >= 0:
            pre_day = self.o_of(pre_i)
            dis = dt // 100 - pre_day // 100
            if dis > 0:
                return True
        return False

    def is_month_end(self, dt):
        current_i = self.i_of(dt)
        next_i = current_i + 1
        if next_i < len(self._cal_list):
            next_day = self.o_of(next_i)
            dis = next_day // 100 - dt // 100
            if dis > 0:
                return True
        return False

    def offset(self, dt, offset=-1):
        current_i = self.i_of(dt)
        offset_i = current_i + offset
        if offset_i >= len(self._cal_list) or offset_i < 0:
            raise IndexError(f'offset index out of range {offset_i}')
        return self.o_of(offset_i)

    def trade_days_count(self, start, end):
        return self.i_of(end) - self.i_of(start)

    def __eq__(self, other):
        return self.cal_list == other.cal_list

    def __len__(self):
        return len(self._cal_list)