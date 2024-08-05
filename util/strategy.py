import datetime

import pandas as pd

import util.time_util as timeutil
import util.util as util


# 日历策略
def calendar_strategy(data, start_date, end_date, params):
    """
    开盘前调用，返回目标组合权重
    Input:
        data: df(date*, index1, index2, ...), basic data
        start_date, end_date: 'yyyy-mm-dd' or datetime.date
        params: dict, format {'index_id':'hs300', 't1':1, 't2':5}
    Output:
        target_wgt: df(trade_date*, index1, index2, ...) 目标权重
    """
    if type(start_date) is str:
        start_date = timeutil.str2date(start_date)
    if type(end_date) is str:
        end_date = timeutil.str2date(end_date)

    index_id = params['index_id']
    t1 = params['t1']
    t2 = params['t2']

    start_date0 = start_date - datetime.timedelta(31)
    dates0 = util.get_trading_dates(start_date0, end_date)
    dates0_rank = util.get_date_count_in_month(dates0)
    target_wgt = pd.DataFrame(data=0, index=dates0, columns=data.columns)
    target_wgt[index_id] = [1 if (e >= t1 and e <= t2) else 0 for e in dates0_rank]
    target_wgt = target_wgt.loc[start_date:end_date]
    return target_wgt


# 轮动策略（可以空仓版）
def rotation_strategy(data, start_date, end_date, params):
    """
    开盘前调用，返回目标组合权重
    Input:
        data: df(date*, index1, index2, ...), basic data
        start_date, end_date: 'yyyy-mm-dd' or datetime.date
        params: dict, format {'index1':'hs300', 'index2':'csi500', 'day':20}
    Output:
        target_wgt: df(trade_date*, index1, index2, ...) 目标权重
    """
    if type(start_date) is str:
        start_date = timeutil.str2date(start_date)
    if type(end_date) is str:
        end_date = timeutil.str2date(end_date)

    day = params['day']
    index1 = params['index1']
    index2 = params['index2']

    start_date0 = start_date - datetime.timedelta(day) * 2
    dates0 = util.get_trading_dates(start_date0, end_date)
    data0 = data.reindex(index=dates0)
    range_day_ret = data0.shift(1) / data0.shift(day + 1) - 1  # 截止昨收的最近 N 个交易日涨幅

    target_wgt = pd.DataFrame(0, index=data0.index, columns=data0.columns)
    for i in range(1, len(target_wgt)):
        t = target_wgt.index[i]
        t0 = target_wgt.index[i - 1]
        index1_last_value = range_day_ret.loc[t0, index1]
        index2_last_value = range_day_ret.loc[t0, index2]
        if index1_last_value >= index2_last_value and index1_last_value > 0:
            target_wgt.loc[t, index1] = 1
        elif index1_last_value < index2_last_value and index2_last_value > 0:
            target_wgt.loc[t, index2] = 1

    target_wgt = target_wgt.loc[start_date:end_date].fillna(0)
    return target_wgt


if __name__ == '__main__':
    data = util.get_history_data()
    start_date = datetime.date(2024, 5, 1)
    end_date = datetime.date(2024, 5, 30)
    # params = {'index_id': 'hs300', 't1': 1, 't2': 5}
    # print(calendar_strategy(data, start_date, end_date, params))

    params = {'day': 20, 'index1': 'hs300', 'index2': 'csi500'}
    print(rotation_strategy(data, start_date, end_date, params))
