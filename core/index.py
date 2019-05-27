# -*- coding: utf-8 -*-
__author__ = "无声"

import time
from core import MultiAdb as Madb
import multiprocessing
from airtest.core.error import *
from poco.exceptions import *


_print = print
def print(*args, **kwargs):
    _print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), *args, **kwargs)

def main():
    madb = Madb.MultiAdb()
    devicesList = madb.devicesList
    if devicesList[0] == "":
        devicesList = madb.getdevices()
    print("测试开始")
    results=""
    if devicesList:
        try:
            pool = multiprocessing.Pool(processes=len(devicesList))
            print("启动进程池")
            results=[]
            for i in range(len(devicesList)):
                pool.apply_async(madb.enter_processing, (i,devicesList[i] ,))  # 根据设备列表去循环创建进程，对每个进程调用下面的enter_processing方法。
            pool.close()
            pool.join()
            print("进程回收完毕")
            print("测试结束")
        except AirtestError as ae:
            print("Airtest发生错误" + ae)
        except PocoException as pe:
            print("Poco发生错误" + pe)
        except Exception as e:
            print("发生未知错误" + e)
    else:
        print("未找到设备，测试结束")






