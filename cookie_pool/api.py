# -*- coding: utf-8 -*-
"""
@Time   : 2018/8/27 18:16
@File   : api.py
@Author : ZZShi
程序作用：
    使用flask框架，提供通过url访问的接口
"""
from flask import Flask, g
from db import RedisClient

from config import *


__all__ = ['app']
app = Flask(__name__)


def get_conn(website):
    if not hasattr(g, 'redis'):
        g.redis = RedisClient('cookies', website)
    return g.redis


@app.route('/')
def index():
    return '<h2>Welcome to Cookies Pool System</h2>'


@app.route('/<website>/random')
def get_cookies(website):
    conn = get_conn(website=website)
    return conn.random()


@app.route('/<website>/count')
def get_count(website):
    conn = get_conn(website)
    return str(conn.len())


if __name__ == '__main__':
    app.run(host=API_HOST, port=API_PORT)



