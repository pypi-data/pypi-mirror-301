import datetime
import pytz


def current_date(days=0):
    """
    获取当前日期：XXXX-XX-XX
    days: 0-代表当天，如果要表示前几天，则 > 0 的对应数字即可；如果要表示后几天，则 < 0 的对应数字即可，
    :return: <class 'datetime.date'>
    """
    current_date_ = datetime.date.today() - datetime.timedelta(days=days)
    return current_date_


def current_time():
    """
    获取当前时间：HH:MM:SS
    :return: str
    """
    now_time = datetime.datetime.now()
    delta = datetime.timedelta(days=0)
    n_date = now_time + delta
    current_time_ = n_date.strftime('%H:%M:%S')
    return current_time_


def date_format(area, source_date):
    """
    转换为标准的日期格式 XXXX-XX-XX HH:MM:SS
    :param area: 地区，用来设置时区的
    :param source_date:
    :return:
    """
    from datetime import datetime
    try:
        date_str = source_date.split('GMT')[0].strip()
        date_ = '%a %b %d %Y %H:%M:%S'
        dt_ = datetime.strptime(date_str, date_)
        # 设置时区
        tz = pytz.timezone(area)
        dt = tz.localize(dt_)
        result_date = dt.strftime('%Y-%m-%d')
    except ValueError:
        result_date = source_date

    return result_date
