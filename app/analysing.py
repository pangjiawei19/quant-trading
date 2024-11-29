import os

import pandas as pd
import matplotlib.pyplot as plt

import util.util as util
from util import time_util

current_directory = os.getcwd()

# 从账户持仓记录表读取持仓市值数据
hold_mv = pd.read_csv(current_directory + '/csv/hold_record.csv').set_index('date')
hold_mv.index = [time_util.str2date(e) for e in hold_mv.index]
start_date = hold_mv.index[0]
end_date = hold_mv.index[-1]

# 化为权重
hold_wgt = hold_mv.iloc[:, 0:-1].copy()
for t in hold_wgt.index:
    hold_wgt.loc[t] = hold_wgt.loc[t] / hold_mv.loc[t, 'amount']

hold_wgt = hold_wgt.loc[:, ['csi1000', 'hs300', 'csi500']]

# 计算净值
data = util.get_history_data(end_date=end_date)
asset_ret = data.pct_change().loc[start_date:end_date]
res = (1 + asset_ret).cumprod()
res['account'] = (1 + (hold_wgt.shift(1) * asset_ret).sum(axis=1)).cumprod()

# 展示净值曲线图和业绩指标表
res.loc[:, ['hs300', 'csi500', 'account']].plot(figsize=(16, 8), grid=True)
results = util.cal_period_perf_indicator(res.loc[:, ['hs300', 'csi500', 'account']])
print(results)

plt.show()
