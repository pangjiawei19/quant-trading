import datetime

import util.strategy as strategy
import util.util as util

T = datetime.date(2024, 11, 1)  # 设置拟交易日期
target_amount = 100000  # 目标投资金额

# 读取基础数据：截止T-1日
data = util.get_history_data(end_date=T - datetime.timedelta(days=1))

# 生成目标组合权重
wgt_calendar_csi1000 = strategy.calendar_strategy(data, T, T,
                                                  params={'index_id': 'csi1000', 't1': 1, 't2': 5})
wgt_rotation_20 = strategy.rotation_strategy(data, T, T,
                                             params={'day': 30, 'index1': 'hs300', 'index2': 'csi500'})
target_wgt = 0.5 * wgt_calendar_csi1000 + 0.5 * wgt_rotation_20  # 多策略目标组合整合
# target_wgt = 1 * wgt_rotation_20  # 多策略目标组合整合

# 输出目标持仓市值
target_mv = target_wgt * target_amount
print('目标持仓市值：')
print(target_mv)
