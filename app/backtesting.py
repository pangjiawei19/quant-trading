import util.strategy as strategy
import util.time_util as time_util
import util.util as util


def test(start_date, end_date, params):
    # 设置回测参数
    if type(start_date) is str:
        start_date = time_util.str2date(start_date)
    if type(end_date) is str:
        end_date = time_util.str2date(end_date)
    index1 = params['index1']
    index2 = params['index2']
    index_account = 'account'

    # 读取基础数据
    data = util.get_history_data(end_date=end_date)

    # 调用策略模块生成目标组合权重
    wgt_calendar_csi1000 = strategy.calendar_strategy(data, start_date, end_date,
                                                      params={'index_id': 'csi1000', 't1': 1, 't2': 5})
    wgt_rotation_20 = strategy.rotation_strategy(data, start_date, end_date, params)
    # target_wgt = 0.5 * wgt_calendar_csi1000 + 0.5 * wgt_rotation_20  # 多策略目标组合整合
    target_wgt = 1 * wgt_rotation_20  # 多策略目标组合整合

    # 产生每日持仓权重
    hold_wgt = target_wgt  # 假设每天都可以准确地执行交易计划

    # 计算组合业绩
    asset_ret = data.pct_change().loc[start_date:end_date]  # 计算各个指标，每天相比于昨天的变化比例
    res = (1 + asset_ret).cumprod()  # 计算各个指标的累计变化率，先加 1 变成针对昨天的比例，再累乘计算为当前日相对于起始日的比例

    hold_asset_ret = hold_wgt.shift(1) * asset_ret  # 昨日持仓权重 * 今日涨跌幅 计算出今日实际的变化比例（如果昨日未持仓，那就是 0）
    account_ret = hold_asset_ret.sum(axis=1)  # 每行按列累计多个指标今日实际变化比例，求和作为总的相比于昨天的变化比例
    account_res = (1 + account_ret).cumprod()  # 计算总比例的累乘，得到当前日相比于起始日的比例
    res[index_account] = account_res

    # 展示净值曲线图和业绩指标表
    res.loc[:, [index1, index2, index_account]].plot(figsize=(16, 8), grid=True)
    performance = util.cal_period_perf_indicator(res.loc[:, [index1, index2, index_account]])
    return performance
