import datetime

import util.strategy as strategy
import util.util as util

data = util.get_history_data()
start_date = datetime.date(2014, 12, 28)
end_date = datetime.date(2024, 1, 1)
params = {'index_id': 'hs300', 't1': 1, 't2': 5}
print(strategy.calendar_strategy(data, start_date, end_date, params))
