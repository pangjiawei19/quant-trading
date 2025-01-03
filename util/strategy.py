import datetime
import math

import pandas as pd

import util.constant as constant
import util.time_util as timeutil
import util.util as util


# 日历策略
def calendar_strategy(data, mode, start_date, end_date, params):
    """
    params: {'codeKeys':['hs300'], 't1':1, 't2':5}
    """
    start_date = timeutil.check_str2date(start_date)
    end_date = timeutil.check_str2date(end_date)

    index_id = params['codeKeys'][0]
    t1 = params['t1']
    t2 = params['t2']

    start_date0 = start_date - datetime.timedelta(31)
    dates0 = util.get_trading_dates(start_date0, end_date)
    dates0_rank = util.get_date_count_in_month(dates0)
    target_wgt = pd.DataFrame(data=0, index=dates0, columns=data.columns)
    target_wgt[index_id] = [1 if (t1 <= e <= t2) else 0 for e in dates0_rank]
    target_wgt = target_wgt.loc[start_date:end_date]
    return target_wgt


def average_strategy(data, mode, start_date, end_date):
    start_date = timeutil.check_str2date(start_date)
    end_date = timeutil.check_str2date(end_date)

    if mode == constant.STRATEGY_EXECUTE_MODE_INVEST:
        dates0 = util.get_trading_dates(start_date, end_date)
        return pd.DataFrame(1, index=dates0, columns=data.columns)

    start_date0 = start_date - datetime.timedelta(2)

    dates0 = util.get_trading_dates(start_date0, end_date)
    data0 = data.reindex(index=dates0)

    target_wgt = pd.DataFrame(0, index=data0.index, columns=data0.columns)
    for t, row in target_wgt.iterrows():
        for column_name in data0.columns:
            if not math.isnan(data0.loc[t, column_name]):
                target_wgt.loc[t, column_name] = 1

    target_wgt = target_wgt.loc[start_date:end_date].fillna(0)
    return target_wgt


def rotation_strategy(data, mode, start_date, end_date, params):
    start_date = timeutil.check_str2date(start_date)
    end_date = timeutil.check_str2date(end_date)

    day = params['day']
    target_count = params.get('target_count', len(data.columns))

    start_date0 = start_date - datetime.timedelta(day) * 2

    dates0 = util.get_trading_dates(start_date0, end_date)
    data0 = data.reindex(index=dates0)
    range_day_ret = data0.shift(1) / data0.shift(day + 1) - 1  # 截止昨收的最近 N 个交易日涨幅

    target_wgt = pd.DataFrame(0, index=data0.index, columns=data0.columns)
    for i in range(1, len(target_wgt)):
        t = target_wgt.index[i]
        t0 = target_wgt.index[i - 1]
        valid_list = []
        for column_name in data0.columns:
            index_last_value = range_day_ret.loc[t0, column_name]
            if not math.isnan(data0.loc[t0, column_name]) and index_last_value > 0:
                valid_list.append({'name': column_name, 'value': index_last_value})
        if len(valid_list) > 0:
            valid_list.sort(key=lambda x: x['value'], reverse=True)
            loop_count = min(target_count, len(valid_list))
            for j in range(0, loop_count):
                target_wgt.loc[t, valid_list[j]['name']] = 1

    target_wgt = target_wgt.loc[start_date:end_date].fillna(0)
    return target_wgt
