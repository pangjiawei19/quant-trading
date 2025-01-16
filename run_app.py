import datetime

import matplotlib.pyplot as plt

import app.app as app
from util import constant

# plt

codeKeys = [
    # constant.TARGET_HS_300,
    # constant.TARGET_CSI_500
    constant.TARGET_HS_300_ETF,
    constant.TARGET_CSI_500_ETF,
    # constant.TARGET_SP_500_ETF,
    constant.TARGET_NAS_100_ETF,
    # constant.TARGET_BOND_ETF
]

strategy_full_calendar = [
    {'type': constant.STRATEGY_CALENDAR, 'weight': 1},
    # {'type': constant.STRATEGY_ROTATION, 'weight': 1},
    # {'type': constant.STRATEGY_AVERAGE, 'weight': 1}
]

strategy_full_rotation = [
    # {'type': constant.STRATEGY_CALENDAR, 'weight': 1},
    {'type': constant.STRATEGY_ROTATION, 'weight': 1},
    # {'type': constant.STRATEGY_AVERAGE, 'weight': 1}
]

strategy_full_average = [
    # {'type': constant.STRATEGY_CALENDAR, 'weight': 1},
    # {'type': constant.STRATEGY_ROTATION, 'weight': 1},
    {'type': constant.STRATEGY_AVERAGE, 'weight': 1}
]

strategy_full_recent_trend = [
    # {'type': constant.STRATEGY_CALENDAR, 'weight': 1},
    # {'type': constant.STRATEGY_ROTATION, 'weight': 1},
    # {'type': constant.STRATEGY_AVERAGE, 'weight': 1}
    {'type': constant.STRATEGY_RECENT_TREND, 'weight': 1}
]

strategy_full_mean_line = [
    # {'type': constant.STRATEGY_CALENDAR, 'weight': 1},
    # {'type': constant.STRATEGY_ROTATION, 'weight': 1},
    # {'type': constant.STRATEGY_AVERAGE, 'weight': 1}
    # {'type': constant.STRATEGY_RECENT_TREND, 'weight': 1}
    {'type': constant.STRATEGY_MEAN_LINE, 'weight': 1}
]

strategy_full_boll_boll = [
    # {'type': constant.STRATEGY_CALENDAR, 'weight': 1},
    # {'type': constant.STRATEGY_ROTATION, 'weight': 1},
    # {'type': constant.STRATEGY_AVERAGE, 'weight': 1}
    # {'type': constant.STRATEGY_RECENT_TREND, 'weight': 1}
    # {'type': constant.STRATEGY_MEAN_LINE, 'weight': 1}
    {'type': constant.STRATEGY_BOLL_BOLL, 'weight': 1}
]

strategy_groups = [
    {
        'name': 'calendar',
        'strategies': strategy_full_calendar
    },
    {
        'name': 'rotation',
        'strategies': strategy_full_rotation
    },
    {
        'name': 'average',
        'strategies': strategy_full_average
    },
    {
        'name': 'recent_trend',
        'strategies': strategy_full_recent_trend
    },
    {
        'name': 'mean_line',
        'strategies': strategy_full_mean_line
    },
    {
        'name': 'boll_boll',
        'strategies': strategy_full_boll_boll
    },
]

params_stg_calendar = {
    't1': 1,
    't2': 5,
}

params_stg_rotation = {
    'day': 20
}

params_stg_recent_trend = {
    'day': 20,
    'long_threshold': 0.05,
    'short_threshold': -0.05,
}

params_stg_mean_line = {
    'n1': 10,
    'n2': 60,
    'long_threshold': 0.05,
    'short_threshold': -0.05,
}

params_stg_boll_boll = {
    'day': 20,
    'multiple': 2
}

params = {
    'codeKeys': codeKeys,
    'invest_strategy': strategy_full_recent_trend,
    'strategy_groups': strategy_groups,
    'params_stg_calendar': params_stg_calendar,
    'params_stg_rotation': params_stg_rotation,
    'params_stg_recent_trend': params_stg_recent_trend,
    'params_stg_mean_line': params_stg_mean_line,
    'params_stg_boll_boll': params_stg_boll_boll
}
# --- backtesting test ---
start_date = datetime.date(2017, 12, 31)  # 回测起始日期
end_date = datetime.date(2024, 10, 31)  # 回测截止日期
results = app.backtest(start_date, end_date, params)
print('回测结果（%s-%s）：' % (start_date, end_date))
print(results)
plt.show()

# # --- invest test ---
# invest_date = datetime.date(2024, 11, 18)  # 设置拟交易日期
# amount = 1000000  # 目标投资金额
# target_hold = app.invest(invest_date, amount, params)
# print('目标持仓市值：')
# print(target_hold)

# --- analyse test ---
# start_date = datetime.date(2025, 1, 1)  # 回测起始日期
# end_date = datetime.date(2025, 2, 1)  # 回测截止日期
# results = app.analyse(params, start_date, end_date)
# print('分析结果（%s-%s）：' % (start_date, end_date))
# print(results)
# plt.show()

# --- record_hold test ---
# hold_info = {constant.TARGET_HS_300_ETF: 0,
#              constant.TARGET_SP_500_ETF: 0,
#              constant.TARGET_CSI_500_ETF: 0,
#              constant.TARGET_NAS_100_ETF: 983087,
#              'amount': 983087}
# record_date = '2025-1-8'
# app.record_hold(hold_info, record_date)

# --- util test ---
# start_date = datetime.date(2023, 12, 25)
# end_date = datetime.date(2024, 1, 5)
# dates = util.get_trading_dates(start_date, end_date)
# print(dates)
# print(util.get_date_count_in_month(dates))
# print(util.get_history_data())
# df = util.get_history_data(['hs300', 'csi1000'], datetime.date(2024, 5, 31))
# print(df)
# print(util.cal_period_perf_indicator(df, True))

# --- strategy test ---
# data = util.get_history_data()
# start_date = datetime.date(2024, 5, 1)
# end_date = datetime.date(2024, 5, 30)
# params = {'index_id': 'hs300', 't1': 1, 't2': 5}
# print(strategy.calendar_strategy(data, start_date, end_date, params))
# params = {'index1': 'hs300', 'index2': 'csi500', 'day': 20}
# hold_wgt = strategy.rotation_strategy(data, start_date, end_date, params)
# print(hold_wgt)
