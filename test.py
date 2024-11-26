import datetime

# import util.strategy as strategy
import util.util as util

#
# data = util.get_history_data()
# start_date = datetime.date(2014, 12, 28)
# end_date = datetime.date(2015, 1, 10)
#
# # params = {'index_id': 'hs300', 't1': 1, 't2': 5}
# # print(strategy.calendar_strategy(data, start_date, end_date, params))
#
# params = {'index1': 'hs300', 'index2': 'csi500', 'day': 20}
# print(strategy.rotation_strategy(data, start_date, end_date, params))

# import app.backtesting as backtesting

# util test
start_date = datetime.date(2023, 12, 25)
end_date = datetime.date(2024, 1, 5)
dates = util.get_trading_dates(start_date, end_date)
print(dates)
print(util.get_date_count_in_month(dates))
print(util.get_history_data())
df = util.get_history_data(['hs300', 'csi1000'], datetime.date(2024, 5, 31))
print(df)
print(util.cal_period_perf_indicator(df))
