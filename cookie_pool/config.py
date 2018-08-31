# -*- coding: utf-8 -*-
"""
@Time   : 2018/8/27 18:14
@File   : config.py
@Author : ZZShi
程序作用：
    配置cookie__pool的一些基本配置，定义全局变量
"""

# 网站名与网站账号
WEBSITE = {'lagou', 'github'}
ACCOUNTS = {
    # 在此填入自己的账号
    'lagou': {
        "username1": "password1",
        "username2": "password2",
        "username3": "password3"
    },
    'github': {
        "username1": "password1",
        "username2": "password2",
        "username3": "password3"
    }
}

# 数据库配置
HOST = 'localhost'
PORT = 6379
DB = 1
PASSWORD = None

# 接口配置
API_HOST = '127.0.0.2'  # 默认为'127.0.0.1'，与代理池的host区分开
API_PORT = 5000

# 运行时间配置
GETTER_CYCLE = 60 * 60 * 24 * 5  # 5天获取一次cookie
TESTER_CYCLE = 60 * 60  # 1小时测试一次cookie是否有效

# 模块使能
GETTER_ENABLE = True
TESTER_ENABLE = True
API_ENABLE = True

