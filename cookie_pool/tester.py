# -*- coding: utf-8 -*-
"""
@Time   : 2018/8/27 18:15
@File   : tester.py
@Author : ZZShi
程序作用：
    测试所有网站和所有账号的cookies是否有效
"""
from db import RedisClient
from login import *
from config import *


class Tester(object):
    """
    测试cookies是否有效
    """
    @staticmethod
    def run():
        for website in ACCOUNTS.keys():
            print('*' * 40)
            print('%s正在检测cookies...' % website)
            acc = RedisClient('accounts', website)
            coo = RedisClient('cookies', website)
            log = eval(website.capitalize() + 'Login()')
            for username, password in acc.get_all().items():
                # 第一次运行时，可能数据还未录入就开始测试，因此加异常处理
                try:
                    cookies = coo.get(username)
                    if log.good_cookies(cookies):
                        print('\t%s\t\tCookies已通过检测...' % username)
                    else:
                        print('\t%s\t\tCookies未通过检测!!!' % username)
                        coo.delete(username)
                        print('\t%s\t\tCookies已删除!!!' % username)
                        log.login(username, password)
                        cookies = log.get_cookies()
                        coo.set(username, cookies)
                except Exception as e:
                    print('数据库为空，请等数据录入之后再进行测试：', e.args)


if __name__ == '__main__':
    t = Tester()
    t.run()
