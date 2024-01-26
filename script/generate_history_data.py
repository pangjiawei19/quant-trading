import akshare as ak

# target = 'sh000300'
# target = 'sh000905'
target = 'sh000852'


# stock_zh_index_daily_tx_df = ak.stock_zh_index_daily_tx(symbol=target)
# print(stock_zh_index_daily_tx_df)

stock_zh_index_daily_df = ak.stock_zh_index_daily(symbol=target)
print(stock_zh_index_daily_df)