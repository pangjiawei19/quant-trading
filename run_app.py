import datetime

import app.app as app

params = {'day': 20, 'index1': 'hs300', 'index2': 'csi500'}
start_date = datetime.date(2014, 1, 1)  # 回测起始日期
end_date = datetime.date(2017, 4, 1)  # 回测截止日期

# --- backtesting test ---
# results = app.backtest(start_date, end_date, params)
# print('回测结果（%s-%s）：' % (start_date, end_date))
# print(results)
# plt.show()

# --- invest test ---
# invest_date = datetime.date(2022, 5, 12)  # 设置拟交易日期
# amount = 100000  # 目标投资金额
# target_hold = app.invest(invest_date, amount, params)
# print('目标持仓市值：')
# print(target_hold)

# --- analyse test ---
# results = app.analyse(params, start_date, end_date)
# print('分析结果（%s-%s）：' % (start_date, end_date))
# print(results)
# plt.show()

# --- record_hold test ---
hold_info = {'hs300': 5000, 'csi500': 50000, 'amount': 200000}
record_date = '2024-12-16'
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
