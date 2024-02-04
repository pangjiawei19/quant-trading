import datetime
import pandas as pd
import util.time_util as timeutil

# target = 'sh000300'
# target = 'sh000905'
target = 'sh000852'

# stock_zh_index_daily_tx_df = ak.stock_zh_index_daily_tx(symbol=target)
# print(stock_zh_index_daily_tx_df)

# stock_zh_index_daily_df = ak.stock_zh_index_daily(symbol=target)
# print(stock_zh_index_daily_df)


csi = pd.read_csv('../csv/csi1000_history.csv').set_index('date')
csi.index = [timeutil.str2date(e) for e in csi.index]
print(csi)

start_date = datetime.date(2005, 1, 31)

csi2 = csi.sort_index().loc[start_date:, ['收盘']]
print(csi2)

# d = csi2.loc[datetime.date(2024, 1, 26), '收盘']
# print(d, type(d), float(d.replace(',', '')), type(float(d.replace(',', ''))))

# df = pd.DataFrame({'month': [1, 4, 7, 10],
#                    'year': [2012, 2014, 2013, 2014],
#                    'sale': [55, 40, 84, 31]})
# print(df)
# df.set_index('month')
# print(df)
