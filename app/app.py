import datetime
import os

import pandas as pd

import util.strategy as strategy
import util.time_util as time_util
import util.util as util

current_directory = os.getcwd()


def generate_target_wgt(data, start_date, end_date, params):
    # 调用策略模块生成目标组合权重
    wgt_calendar_csi1000 = strategy.calendar_strategy(data, start_date, end_date,
                                                      params={'index_id': 'csi1000', 't1': 1, 't2': 5})
    wgt_rotation_20 = strategy.rotation_strategy(data, start_date, end_date, params)

    # target_wgt = 0.5 * wgt_calendar_csi1000 + 0.5 * wgt_rotation_20  # 多策略目标组合整合
    target_wgt = 1 * wgt_rotation_20  # 多策略目标组合整合

    return target_wgt


def calculate_performance(start_date, end_date, hold_wgt, params):
    index1 = params['index1']
    index2 = params['index2']
    index_account = 'account'

    data = util.get_history_data([index1, index2], end_date=end_date)
    asset_ret = data.pct_change().loc[start_date:end_date]
    res = (1 + asset_ret).cumprod()

    hold_asset_ret = hold_wgt.shift(1) * asset_ret
    account_ret = hold_asset_ret.sum(axis=1)
    account_res = (1 + account_ret).cumprod()
    res[index_account] = account_res

    # 展示净值曲线图和业绩指标表
    res.loc[:, [index1, index2, index_account]].plot(figsize=(16, 8), grid=True)
    performance = util.cal_period_perf_indicator(res.loc[:, [index1, index2, index_account]])
    return performance


def backtest(start_date, end_date, params):
    index1 = params['index1']
    index2 = params['index2']
    # 设置回测参数
    start_date = time_util.check_str2date(start_date)
    end_date = time_util.check_str2date(end_date)

    # 读取基础数据
    data = util.get_history_data([index1, index2], end_date=end_date)

    # 调用策略模块生成目标组合权重
    hold_wgt = generate_target_wgt(data, start_date, end_date, params)  # 假设每天都可以准确地执行交易计划

    # 展示换手情况
    hold_wgt[[index1, index2]].plot(figsize=(16, 8), kind='area', stacked=True, grid=True)

    # 计算组合业绩
    return calculate_performance(start_date, end_date, hold_wgt, params)


def invest(date, target_amount, params):
    index1 = params['index1']
    index2 = params['index2']
    date = time_util.check_str2date(date)  # 设置拟交易日期

    # 读取基础数据：截止T-1日
    data = util.get_history_data([index1, index2], end_date=date - datetime.timedelta(days=1))

    # 生成目标组合权重
    target_wgt = generate_target_wgt(data, date, date, params)

    # 输出目标持仓市值
    target_mv = target_wgt * target_amount
    return target_mv


def analyse(params, start_date=None, end_date=None):
    index1 = params['index1']
    index2 = params['index2']
    # 从账户持仓记录表读取持仓市值数据
    hold_mv = pd.read_csv(current_directory + '/csv/hold_record.csv').set_index('date')
    hold_mv.index = [time_util.str2date(e) for e in hold_mv.index]
    if start_date is None:
        start_date = hold_mv.index[0]
    if end_date is None:
        end_date = hold_mv.index[-1]

    # 化为权重
    hold_wgt = hold_mv.iloc[:, 0:-1].copy()
    for t in hold_wgt.index:
        hold_wgt.loc[t] = hold_wgt.loc[t] / hold_mv.loc[t, 'amount']

    hold_wgt = hold_wgt.loc[start_date:end_date, [index1, index2]]

    # 计算净值
    return calculate_performance(start_date, end_date, hold_wgt, params)


def record_hold(hold_info, record_date):
    record_date = time_util.check_str2date(record_date)
    hold_mv = pd.read_csv(current_directory + '/csv/hold_record.csv').set_index('date')
    hold_mv.index = [time_util.str2date(e) for e in hold_mv.index]

    start_date = record_date
    if len(hold_mv) > 0:
        start_date = hold_mv.index[-1] + datetime.timedelta(days=1)
    trading_dates = util.get_trading_dates(start_date, record_date)

    for date in trading_dates:
        for index in hold_info.keys():
            hold_mv.loc[date, index] = hold_info[index]

    hold_mv = hold_mv.fillna(0)
    hold_mv.to_csv(current_directory + '/csv/hold_record.csv', index_label='date', header=True)
