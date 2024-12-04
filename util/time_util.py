import datetime


def str2date(datestr, format='%Y-%m-%d'):
    # 日期格式转换：'yyyy-mm-dd'转为datetime.date
    return datetime.datetime.strptime(datestr, format).date()


def check_str2date(date, format='%Y-%m-%d'):
    if type(date) is str:
        return str2date(date, format)
    else:
        return date
