import datetime
import os

import akshare as ak
import numpy as np
import pandas as pd

from util import time_util

current_directory = os.getcwd()

CODE_DICT = {
    'csi1000': 'sh000852',
    'hs300': 'sh000300',
    'csi500': 'sh000905',
    'hs300Etf': 'sh510300',
    'csi500Etf': 'sz159922',
    'sp500Etf': 'sh513500',
    'nas100Etf': 'sz159513',
    'bondEtf': 'sh511010'
}
BASIC_DATA_START_DATE = datetime.date(2005, 2, 1)


# 读取指定起止日期之间的交易日序列
def get_trading_dates(start_date=None, end_date=None):
    dates = pd.read_csv(current_directory + '/csv/trading_date.csv')['trade_date'].to_list()
    dates = [time_util.str2date(e, '%Y-%m-%d') for e in dates]
    if start_date is not None:
        dates = [e for e in dates if e >= start_date]
    if end_date is not None:
        dates = [e for e in dates if e <= end_date]
    return dates


def is_trading_date(date):
    dates = pd.read_csv(current_directory + '/csv/trading_date.csv')['trade_date'].to_list()
    dates = [time_util.str2date(e, '%Y-%m-%d') for e in dates]
    return date in dates


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
    # data = pd.read_csv(current_directory + '/csv/basic_data.csv').set_index('datetime')
    # data.index = [time_util.str2date(e) for e in data.index]

    # 动态获取指数价格数据
    codeKeys = index_ids if index_ids is not None else CODE_DICT.keys()
    data = generate_basic_data(codeKeys)

    if index_ids is not None:
        data = data.loc[:, index_ids]
    if end_date is not None:
        data = data.loc[:end_date, :]
    return data


def get_drawdown(p):
    """
    计算净值回撤
    """
    hmax = p.cummax()  # 从序列开始到该元素位置的最大值，这是一个与 p 长度相同的 Pandas Series，每个元素表示从序列开始到该点的最大净值
    dd = p / hmax - 1  # 当前净值相对于累计最大值的百分比跌幅

    return dd  # 每个元素表示对应时间点的回撤


def cal_period_perf_indicator(data, is_real_value=False):
    """
    计算区间业绩指标:输入必须是日频净值
    """
    if isinstance(data, pd.DataFrame):
        res = pd.DataFrame(index=data.columns,
                           columns=['AnnRet', 'AnnVol', 'SR', 'MaxDD', 'Calmar'])  # 创建新的 df，index 是 data 的列名，即指数名称
        for col in data:
            res.loc[col] = cal_period_perf_indicator(data[col], is_real_value)  # 递归调用，计算每个指数（每行）的业绩指标
        return res

    ret = data.pct_change()
    init_value = (data.iloc[0] if is_real_value else 1)
    # annret = np.nanmean(ret) * 242 # 单利
    # annret = (data.iloc[-1] / 1) ** (242 / len(data)) - 1  # 年化收益率（Annual Return），表示一年内的平均收益
    annret = (data.iloc[-1] / init_value) ** (242 / len(data)) - 1  # 年化收益率（Annual Return），表示一年内的平均收益
    annvol = np.nanstd(ret) * np.sqrt(242)  # 年化波动率（AnnVol），表示收益的波动性
    sr = annret / annvol  # 夏普比率（Sharpe Ratio），收益相比于波动的比例，表示风险下的回报
    dd = get_drawdown(data)  # 回撤（Maximum Drawdown），一段时间内各个时间点的回撤
    mdd = np.nanmin(dd)  # 最大回撤（Max Drawdown），表示在一段时间内从峰值到谷底的最大跌幅
    calmar = annret / -mdd  # 卡尔玛比率（Calmar Ratio），年化收益率与最大回撤的比率，表示单位最大回撤下的收益

    return [annret, annvol, sr, mdd, calmar]


def generate_history_data_by_code(code, start_date):
    daily_df = ak.stock_zh_index_daily(symbol=code).set_index('date').loc[start_date:, ['close']]
    if code == CODE_DICT['csi1000']:
        history_df = pd.read_csv(current_directory + '/csv/csi1000_history.csv').set_index('date')
        history_df.index = [time_util.str2date(e) for e in history_df.index]
        history_df = history_df.loc[start_date:, ['close']]
        daily_df = daily_df.combine_first(history_df)

    return daily_df


def generate_basic_data(codeKeys, start_date=BASIC_DATA_START_DATE):
    data = pd.DataFrame()
    for key in codeKeys:
        daily_df = generate_history_data_by_code(CODE_DICT[key], start_date)
        data[key] = daily_df['close']
    return data
