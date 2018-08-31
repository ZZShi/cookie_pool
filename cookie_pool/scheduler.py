# -*- coding: utf-8 -*-
"""
@Time   : 2018/8/27 18:16
@File   : scheduler.py
@Author : ZZShi
程序作用：
    实现获取、测试、调用的调度
"""
import time
from multiprocessing import Process
from config import *
from getter import Getter
from tester import Tester
from api import app


class Scheduler(object):
    """
    调度类，实现Getter、Tester、app三个对象的调度
    """
    def __init__(self):
        self.getter_cycle = GETTER_CYCLE
        self.tester_cycle = TESTER_CYCLE

    def scheduler_getter(self):
        """
        每隔5天获取一次cookies
        :return:
        """
        while True:
            getter = Getter()
            getter.run()
            time.sleep(self.getter_cycle)

    def scheduler_tester(self):
        """
        每隔1小时检测一下cookies是否有效
        :return:
        """
        while True:
            tester = Tester()
            tester.run()
            time.sleep(self.getter_cycle)

    @staticmethod
    def scheduler_api():
        """
        保持调用接口一直打开
        :return:
        """
        app.run(host=API_HOST, port=API_PORT)

    def run(self):
        """
        使用多进程方式使三个进程同时运行
        :return:
        """
        print('Cookies Pool System is running...')
        ps = []
        if GETTER_ENABLE:
            p = Process(target=self.scheduler_getter)
            p.start()
        if TESTER_ENABLE:
            p = Process(target=self.scheduler_tester)
            p.start()
        if API_ENABLE:
            p = Process(target=self.scheduler_api)
            p.start()
        for p in ps:
            p.join()


if __name__ == '__main__':
    s = Scheduler()
    s.run()

