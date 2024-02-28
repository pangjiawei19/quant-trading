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


if __name__ == '__main__':
    data = util.get_history_data()
    start_date = datetime.date(2015, 1, 1)
    end_date = datetime.date(2024, 1, 1)
    params = {'index_id': 'hs300', 't1': 1, 't2': 5}
    print(calendar_strategy(data, start_date, end_date, params))
