import datetime
import matplotlib.pyplot as plt

# --- backtesting test ---
import app.backtesting as backtesting

start_date = datetime.date(2022, 1, 1)  # 回测起始日期
end_date = datetime.date(2024, 11, 1)  # 回测截止日期
params = {'day': 20, 'index1': 'hs300', 'index2': 'csi500'}
results = backtesting.test(start_date, end_date, params)
print(results)
plt.show()

# --- invest test ---
# import app.investing as investing

# --- analyse test ---
# import app.analysing as analysing


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
# print(strategy.rotation_strategy(data, start_date, end_date, params))
