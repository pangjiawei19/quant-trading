import datetime
import akshare as ak
import pandas as pd

import util.time_util as timeutil

# target = 'sh000300'
# target = 'sh000905'
target = 'sh000852'  # csi1000
csi1000_code = 'sh000852'

# stock_zh_index_daily_tx_df = ak.stock_zh_index_daily_tx(symbol=target)
# print(stock_zh_index_daily_tx_df)

# stock_zh_index_daily_df = ak.stock_zh_index_daily(symbol=target)
# print(stock_zh_index_daily_df)

start_date = datetime.date(2005, 2, 1)

csi1000_history = pd.read_csv('../csv/csi1000_history.csv').set_index('date')
csi1000_history.index = [timeutil.str2date(e) for e in csi1000_history.index]

csi1000_history_df = csi1000_history.loc[start_date:, ['close']]
print(csi1000_history_df)

csi1000_daily_df = ak.stock_zh_index_daily(symbol=csi1000_code).set_index('date').loc[start_date:, ['close']]
print(csi1000_daily_df)

csi1000 = csi1000_daily_df.combine_first(csi1000_history_df)
print(csi1000)
