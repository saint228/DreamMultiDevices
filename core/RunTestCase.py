# -*- coding: utf-8 -*-
__author__ = "无声"
#import os
#import time
import unittest
from BeautifulReport import BeautifulReport
from airtest.core.api import *
from DreamMultiDevices.tools import File
from DreamMultiDevices.TestCase import *
_print = print
def print(*args, **kwargs):
    _print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), *args, **kwargs)

#运行Testcase的主函数
def RunTestCase(madb,start):
    devices=madb.get_mdevice()
    print("进入{}的RunTestCase".format(devices))
    # 获取路径
    package = madb.get_packagename()
    TestCasePath = madb.get_TestCasePath()
    print("TestCasePath=",TestCasePath)
    if not os.path.exists(TestCasePath):
        print("测试用例需放到‘TestCase’文件目录下")
    reportpath = os.path.join(os.getcwd(), "Report")
    #没有Report目录时自动创建
    if not os.path.exists(reportpath):
        os.mkdir(reportpath)
        os.mkdir(reportpath+"/Screen")
    #读取ini文件，获得期望测试的用例列表
    TestList=madb.get_testcaseforselfdevice()
    print("{}的待测用例为：{}".format(madb.get_mdevice(),TestList))
    # 通过GetPyList方法，取得目录里可测试的用例列表
    scriptList = File.GetPyList(TestCasePath)
    suite = unittest.TestSuite()
    for i in range(len(TestList)):
        fileName = "TC_" + TestList[i]
        print("fileName=",fileName)
        if fileName in scriptList:
            print("进入循环")
            #在整个命名空间里遍历所有名称为"TC_xx.py"形式的文件，默认这些文件都是unittest测试文件，然后调用其Main函数。
            result = globals()[fileName].Main(devices)
            suite.addTests(result)
    #聚合报告到BR
    unittestReport = BeautifulReport(suite)
    nowtime=time.strftime("%H%M%S",start)
    #unittestReport.report(filename=madb.get_nickdevice()+"_"+str(nowtime),description=package, report_dir=reportpath,rundevice=madb.get_mdevice())
    unittestReport.report(filename=madb.get_nickname()+"_"+str(nowtime),description=package, report_dir=reportpath)
    stop_app(package)



