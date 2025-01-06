import akshare as ak

df = ak.tool_trade_date_hist_sina()

print(df)
df.to_csv('csv/trading_date.csv', index=True, header=True)
