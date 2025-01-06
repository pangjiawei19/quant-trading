import datetime

import app.app as app
from util import constant
import matplotlib.pyplot as plt

codeKeys = [
    # constant.TARGET_HS_300,
    # constant.TARGET_CSI_500
    constant.TARGET_HS_300_ETF,
    constant.TARGET_CSI_500_ETF,
    constant.TARGET_SP_500_ETF,
    constant.TARGET_NAS_100_ETF,
    # constant.TARGET_BOND_ETF
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

strategy_groups = [
    {
        'name': 'rotation',
        'strategies': strategy_full_rotation
    },
    {
        'name': 'average',
        'strategies': strategy_full_average
    }
]

params = {'day': 20, 't1': 1, 't2': 5,
          'codeKeys': codeKeys,
          'invest_strategy': strategy_full_rotation,
          'strategy_groups': strategy_groups,
          'target_count': 100}
# --- backtesting test ---
# start_date = datetime.date(2009, 1, 1)  # 回测起始日期
# end_date = datetime.date(2024, 12, 1)  # 回测截止日期
# results = app.backtest(start_date, end_date, params)
# print('回测结果（%s-%s）：' % (start_date, end_date))
# print(results)
# plt.show()

# # --- invest test ---
# invest_date = datetime.date(2025, 1, 6)  # 设置拟交易日期
# amount = 5000  # 目标投资金额
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
hold_info = {constant.TARGET_HS_300_ETF: 5365,
             constant.TARGET_SP_500_ETF: 6190,
             constant.TARGET_CSI_500_ETF: 4873,
             constant.TARGET_NAS_100_ETF: 5959,
             'amount': 22389}
record_date = '2025-2-6'
app.record_hold(hold_info, record_date)

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
