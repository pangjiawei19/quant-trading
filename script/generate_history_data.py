from util import util

basic = util.generate_basic_data(util.CODE_DICT.keys())

print(basic)
basic.to_csv('csv/basic_data.csv', index_label='datetime')
