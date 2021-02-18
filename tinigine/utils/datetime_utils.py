"""
@project: tinigine
@author: kang
@github: https://github.com/fsksf 
@since: 2021/2/18 5:43 PM
"""
import datetime


def to_datetime(s: str) -> datetime.datetime:
    s = str(s)
    if len(s) == 8:
        dt = datetime.datetime.strptime(str(s), '%Y%m%d')
    else:
        dt = datetime.datetime.strptime(str(s), '%Y%m%d%H%M%S')
    return dt


def day_count(start, end):
    start_date = to_datetime(start).date()
    end_date = to_datetime(end).date()
    dalt = (end_date - start_date)
    return dalt.days