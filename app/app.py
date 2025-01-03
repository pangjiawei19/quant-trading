import datetime
import os

import pandas as pd

import util.constant as constant
import util.strategy as strategy
import util.time_util as time_util
import util.util as util

current_directory = os.getcwd()


def generate_target_wgt(data, mode, start_date, end_date, params, strategies):
    target_wgt = None

    for stegy in strategies:
        strategy_type = stegy['type']
        strategy_wgt = pd.DataFrame()
        if strategy_type == constant.STRATEGY_CALENDAR:
            strategy_wgt = strategy.calendar_strategy(data, mode, start_date, end_date, params)
        elif strategy_type == constant.STRATEGY_ROTATION:
            strategy_wgt = strategy.rotation_strategy(data, mode, start_date, end_date, params)
        elif strategy_type == constant.STRATEGY_AVERAGE:
            strategy_wgt = strategy.average_strategy(data, mode, start_date, end_date)

        if target_wgt is None:
            target_wgt = stegy['weight'] * strategy_wgt
        else:
            target_wgt += stegy['weight'] * strategy_wgt

    # print(target_wgt)
    return target_wgt


def calculate_performance(start_date, end_date, hold_weights, code_keys):
    data = util.get_history_data(code_keys, end_date=end_date)
    asset_ret = data.pct_change().loc[start_date:end_date]
    res = (1 + asset_ret).cumprod()

    for hold_wgt in hold_weights:
        hold_asset_ret = hold_wgt['data'].shift(1) * asset_ret
        account_ret = hold_asset_ret.sum(axis=1)
        account_res = (1 + account_ret).cumprod()
        res[hold_wgt['name']] = account_res

    # 展示净值曲线图和业绩指标表
    # newColumns = params['codeKeys'] + [index_account]
    # res = res.loc[:, newColumns]
    res.plot(figsize=(16, 8), grid=True)
    performance = util.cal_period_perf_indicator(res)
    return performance


def backtest(start_date, end_date, params):
    # 设置回测参数
    start_date = time_util.check_str2date(start_date)
    end_date = time_util.check_str2date(end_date)

    # 读取基础数据
    code_keys = params['codeKeys']
    data = util.get_history_data(code_keys, end_date=end_date)

    # 计算组合业绩
    hold_weights = []
    for strategy_group in params['strategy_groups']:
        # 生成目标组合权重，假设每天都可以准确地执行交易计划
        hold_wgt = generate_target_wgt(data, constant.STRATEGY_EXECUTE_MODE_BACKTEST,
                                       start_date, end_date,
                                       params, strategy_group['strategies'])
        name = strategy_group['name']
        hold_weights.append({'name': name, 'data': hold_wgt})

        # 展示换手情况
        hold_wgt[code_keys].plot(figsize=(16, 8), title=name, kind='area', stacked=True, grid=True)

    return calculate_performance(start_date, end_date, hold_weights, code_keys)


def invest(date, target_amount, params):
    date = time_util.check_str2date(date)  # 设置拟交易日期

    # 读取基础数据：截止T-1日
    code_keys = params['codeKeys']
    data = util.get_history_data(code_keys, end_date=date - datetime.timedelta(days=1))

    # 生成目标组合权重
    target_wgt = generate_target_wgt(data, constant.STRATEGY_EXECUTE_MODE_INVEST, date, date, params,
                                     params['invest_strategy'])

    # 输出目标持仓市值
    valid_count = 0
    for codeKey in code_keys:
        if target_wgt.loc[date, codeKey] > 0:
            valid_count += 1
    if valid_count < 1:
        return target_wgt * target_amount

    return target_wgt * (target_amount / valid_count)


def analyse(params, start_date=None, end_date=None):
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

    code_keys = params['codeKeys']
    hold_wgt = hold_wgt.loc[start_date:end_date, code_keys]
    hold_weights = [{'name': 'hold', 'data': hold_wgt}]

    # 计算净值
    return calculate_performance(start_date, end_date, hold_weights, code_keys)


def record_hold(hold_info, record_date):
    record_date = time_util.check_str2date(record_date)
    hold_mv = pd.read_csv(current_directory + '/csv/hold_record.csv').set_index('date')
    hold_mv.index = [time_util.str2date(e) for e in hold_mv.index]

    # 中间空缺记录
    if len(hold_mv) > 0:
        start_date = hold_mv.index[-1] + datetime.timedelta(days=1)
        end_date = record_date - datetime.timedelta(days=1)
        trading_dates = util.get_trading_dates(start_date, end_date)

        for date in trading_dates:
            hold_mv.loc[date] = hold_mv.iloc[-1]

    # 当天
    if util.is_trading_date(record_date):
        for index in hold_info.keys():
            hold_mv.loc[record_date, index] = hold_info[index]

    hold_mv = hold_mv.fillna(0)
    hold_mv.to_csv(current_directory + '/csv/hold_record.csv', index_label='date', header=True)
