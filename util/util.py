import datetime
import os

import pandas as pd

import util.time_util as timeutil

current_directory = os.getcwd()


# 读取指定起止日期之间的交易日序列
def get_trading_dates(start_date=None, end_date=None):
    dates = pd.read_csv(current_directory + '/csv/trading_date.csv')['trade_date'].to_list()
    dates = [timeutil.str2date(e, '%Y-%m-%d') for e in dates]
    if start_date is not None:
        dates = [e for e in dates if e >= start_date]
    if end_date is not None:
        dates = [e for e in dates if e <= end_date]
    return dates


# 计算日期序列中每个日期在所在月中的序数
def get_date_count_in_month(dates):
    cur_count = 1
    counts = [cur_count]
    for i in range(1, len(dates)):
        if dates[i].month == dates[i - 1].month:
            cur_count = cur_count + 1
        else:
            cur_count = 1
        counts.append(cur_count)
    return counts


def get_history_data(index_ids=None, end_date=None):
    """
    读取指数历史数据到指定截止日

    Input:
        index_ids: list of str, 指数代码列表, like ['hs300', 'csi500']
        end_date: datetime.date, 截止日期
    Output:
        data: df(date*, index1, index2, ...), 多个指数的历史收盘价序列
    """
    # 从csv文件获取指数价格数据
    data = pd.read_csv(current_directory + '/csv/basic_data.csv').set_index('datetime')
    data.index = [timeutil.str2date(e) for e in data.index]
    if index_ids is not None:
        data = data.loc[:, index_ids]
    if end_date is not None:
        data = data.loc[:end_date, :]
    return data


if __name__ == '__main__':
    start_date = datetime.date(2023, 12, 25)
    end_date = datetime.date(2024, 1, 5)
    dates = get_trading_dates(start_date, end_date)
    print(dates)
    print(get_date_count_in_month(dates))
    print(get_history_data())
    print(get_history_data(['hs300', 'csi1000'], datetime.date(2021, 1, 1)))
