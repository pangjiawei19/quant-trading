import datetime


def str2date(datestr, format='%Y-%m-%d'):
    # 日期格式转换：'yyyy-mm-dd'转为datetime.date
    return datetime.datetime.strptime(datestr, format).date()
