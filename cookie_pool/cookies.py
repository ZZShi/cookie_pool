# -*- coding: utf-8 -*-
"""
@Time   : 2018/8/27 18:16
@File   : cookies.py
@Author : ZZShi
程序作用：
    提供两种调用方式，url或数据库
"""
from scheduler import Scheduler
from db import RedisClient


def start_cps():
    """
    启动Cookies Pool System
    启动之后便可以访问http://127.0.0.2:5000/<website>/random 获取该网站的随机cookies
    :return:
    """
    s = Scheduler()
    s.run()


def get_cookies_from_db(website):
    """
    提供此方法可以直接从数据库获取随机cookies
    :param website: 网站，全小写
    :return: 该网站的随机cookies,str类型，需要转换成Dict或CookieJar对象才能使用
    """
    acc = RedisClient('cookies', website)
    return acc.random()


if __name__ == '__main__':
    for _ in range(5):
        cookies = get_cookies_from_db('lagou')
        print(cookies)

