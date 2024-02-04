import pandas as pd

import util.time_util as timeutil

csi = pd.read_csv('../csv/csi1000_history_origin.csv').set_index('date')
csi.index = [timeutil.str2date(e) for e in csi.index]
csi = csi.sort_index()
print(csi)

csi2 = pd.DataFrame()

csi2['start'] = csi['开盘'].str.replace(',', '')
csi2['close'] = csi['收盘'].str.replace(',', '')
csi2['max'] = csi['高'].str.replace(',', '')
csi2['min'] = csi['低'].str.replace(',', '')

print(csi2)

csi2.to_csv('../csv/csi1000_history.csv', index=True, header=True)
