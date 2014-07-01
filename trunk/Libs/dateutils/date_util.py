# -*- coding: utf-8 -*-

from datetime import timedelta, date


def pre_month(date):
    return (date.replace(day=1) - timedelta(1)).replace(day=1)


def next_month(date):
    return (date.replace(day=1) + timedelta(32)).replace(day=1)


if __name__ == '__main__':
    d1 = date(2012, 1, 30)

    print next_month(d1)

    import datetime

    d2 = datetime.datetime.strptime('2012-12', '%Y-%m')
    print d2
