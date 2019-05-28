# -*- coding: utf-8 -*-
__author__ = "无声"

import unittest
import time
from BeautifulReport import BeautifulReport
import os
from airtest.core.api import *
from tools import  File
from TestCase import *
_print = print
def print(*args, **kwargs):
    _print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), *args, **kwargs)

def RunTestCase(madb):
    devices=madb.get_mdevice()
    print("进入{}的RunTestCase".format(devices))
    # 获取路径
    package = madb.get_packagename()
    casepath = os.path.join(os.getcwd(), "TestCase")
    print("casepath=",casepath)
    if not os.path.exists(casepath):
        print("测试用例需放到‘TestCase’文件目录下")
    reportpath = os.path.join(os.getcwd(), "Report")
    if not os.path.exists(reportpath):
        os.mkdir(reportpath)
        os.mkdir(reportpath+"/Screen")
    #读取ini文件，获得期望测试的用例列表
    TestList=madb.get_alltestcase()
    # 通过GetPyList方法，取得目录里可测试的用例列表
    scriptList = File.GetPyList(casepath)
    suite = unittest.TestSuite()
    for i in range(len(TestList)):
        fileName = "TC_" + TestList[i]
        if fileName in scriptList:
            result = globals()[fileName].Main(devices)
            suite.addTests(result)
    unittestReport = BeautifulReport(suite)
    #处理模拟器端口用的冒号
    if ":" in devices:
        devices=devices.split(":")[1]
    nowtime=time.strftime("%H%M%S")
    unittestReport.report(filename=devices+"_"+str(nowtime),description=package, report_dir=reportpath)
    stop_app(package)


#RunTestCase(time.time(),"127.0.0.1:62001")
