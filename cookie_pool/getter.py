# -*- coding: utf-8 -*-
"""
@Time   : 2018/8/27 18:15
@File   : getter.py
@Author : ZZShi
程序作用：
    定义一个Getter类，实现账号录入到数据库可模拟登陆保存cookies到数据库
"""
from config import *
from db import RedisClient
from login import *


class Getter(object):
    """
    保存账号和cookies到数据库
    """

    @staticmethod
    def save_accounts():
        """
        录入账号和密码
        :return:
        """
        for website, accounts in ACCOUNTS.items():
            acc = RedisClient('accounts', website)
            acc.set_many(accounts)
            print('%s的所有账号已保存成功...' % website)

    @staticmethod
    def save_cookies():
        """
        录入账号和cookies
        :return:
        """
        print('*' * 40)
        for website in ACCOUNTS.keys():
            print('%s正在获取cookies...' % website)
            acc = RedisClient('accounts', website)
            coo = RedisClient('cookies', website)
            for username, password in acc.get_all().items():
                log = eval(website.capitalize() + 'Login()')
                log.login(username, password)
                cookies = log.get_cookies()
                coo.set(username, cookies)
            print('%s的所有cookies已保存成功...' % website)
            print('*' * 40)

    def run(self):
        self.save_accounts()
        self.save_cookies()


if __name__ == '__main__':
    g = Getter()
    g.run()
