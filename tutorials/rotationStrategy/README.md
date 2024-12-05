# RotationStrategy
轮动策略回测：数据，回测程序

满仓版本：
沪深 300 指数代表大盘股，中证 500 指数代表中小盘股。每天回看这两个指数最近 20 个交易日的涨幅，当沪深 300 的区间涨幅大于中证 500 时，持有沪深 300；当中证 500 的区间涨幅大于沪深 300 时，持有中证 500。

可空仓版本：
与前面版本的唯一差异就是，当回看 20 个交易日涨幅时，如果两个指数均为下跌，就选择空仓。