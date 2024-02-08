import datetime

import akshare as ak
import pandas as pd

import util.time_util as timeutil

csi1000_code = 'sh000852'
hs300_code = 'sh000300'
csi500_code = 'sh000905'

start_date = datetime.date(2005, 2, 1)


def generate_csi1000(start_date):
    history_df = pd.read_csv('../csv/csi1000_history.csv').set_index('date')
    history_df.index = [timeutil.str2date(e) for e in history_df.index]
    history_df = history_df.loc[start_date:, ['close']]

    daily_df = ak.stock_zh_index_daily(symbol=csi1000_code).set_index('date').loc[start_date:, ['close']]

    df = daily_df.combine_first(history_df)
    return df


def generate_hs300(start_date):
    daily_df = ak.stock_zh_index_daily(symbol=hs300_code).set_index('date').loc[start_date:, ['close']]
    return daily_df

def generate_csi500(start_date):
    daily_df = ak.stock_zh_index_daily(symbol=csi500_code).set_index('date').loc[start_date:, ['close']]
    return daily_df


csi1000 = generate_csi1000(start_date)
hs300 = generate_hs300(start_date)
csi500 = generate_csi500(start_date)


basic = pd.DataFrame()
basic['csi1000'] = csi1000['close']
basic['hs300'] = hs300['close']
basic['csi500'] = csi500['close']

print(basic)

basic.to_csv('../csv/basic_data.csv', index_label='datetime')
