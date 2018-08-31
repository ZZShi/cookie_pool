# -*- coding: utf-8 -*-
"""
@Time   : 2018/8/27 18:15
@File   : db.py
@Author : ZZShi
程序作用：
    定义Redis数据库的增删查改功能
"""
import redis
from random import choice

from config import *


class RedisClient(object):
    def __init__(self, content, website, host=HOST, port=PORT, db=DB, password=PASSWORD):
        """
        数据库初始化
        :param content: accounts or cookies
        :param website: 网站名
        :param host:
        :param port:
        :param db:
        :param password:
        """
        self.content = content
        self.website = website

        self.redis = redis.StrictRedis(host=host, port=port, db=db, password=password)

    def name(self):
        """
        定义哈希表的名称
        :return:
        """
        return '{}:{}'.format(self.content, self.website)

    def set(self, key, value):
        """
        添加将一组键值对
        :param key: username
        :param value: password or cookies
        :return:
        """
        return self.redis.hset(self.name(), key, value)

    def set_many(self, mapping):
        """
        添加多组键值对
        :param mapping: dict or json 类型，添加账号字典比较合适
        :return:
        """
        return self.redis.hmset(self.name(), mapping)

    def delete(self, key):
        """
        删除一组键值对
        :param key:
        :return:
        """
        return self.redis.hdel(self.name(), key)

    def get(self, key):
        """
        得到key对应的值
        :param key:
        :return:
        """
        return self.redis.hget(self.name(), key).decode('utf-8')

    def get_all(self):
        """
        得到哈希表的所有key、value
        :return:
        """
        decode_dict = {}
        for username, password in self.redis.hgetall(self.name()).items():
            username = username.decode('utf-8')
            password = password.decode('utf-8')
            decode_dict[username] = password
        return decode_dict

    def random(self):
        """
        随机得到散列表的值
        :return:
        """
        return choice(self.redis.hvals(self.name())).decode('utf-8')

    def exist(self, key):
        """
        判断该键值是否存在
        :param key:
        :return:
        """
        return self.redis.hexists(self.name(), key)

    def len(self):
        """
        得到哈希表的映射个数
        :return:
        """
        return self.redis.hlen(self.name())


if __name__ == '__main__':
    for website in WEBSITE:
        acc = RedisClient('accounts', website)
        accounts = ACCOUNTS.get(website)
        acc.set_many(accounts)
        print(accounts)
