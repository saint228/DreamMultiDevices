# -*- coding: utf-8 -*-
__author__ = "无声"

import unittest
from tools import  Screencap
from airtest.core.api import *
_print = print
def print(*args, **kwargs):
    _print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), *args, **kwargs)
def Main(devices):
    class TC101(unittest.TestCase):
        u'''测试用例101的集合'''

        @classmethod
        def setUpClass(self):
            u''' 这里放需要在所有用例执行前执行的部分'''
            pass

        def setUp(self):
            u'''这里放需要在每条用例前执行的部分'''
            print("我是setUp，在每条用例之前执行")

        def test_01_of_101(self):
            u'''用例test_01_of_101的操作步骤'''
            t = 1
            self.assertEquals(1, t)

        def test_02_of_101(self):
            u'''用例test_02_of_101的操作步骤'''
            time.sleep(5)
            Screencap.GetScreen(time.time(), devices, "test_02_of_101的描述")
            t = 1
            self.assertEquals(2, t)


        def tearDown(self):
            u'''这里放需要在每条用例后执行的部分'''
            print("tearDown，在每条用例之后执行")

        @classmethod
        def tearDownClass(self):
            u'''这里放需要在所有用例后执行的部分'''
            pass

    srcSuite = unittest.makeSuite(TC101)
    return srcSuite