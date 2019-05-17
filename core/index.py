# -*- coding: utf-8 -*-
__author__ = "无声"

import multiprocessing
from airtest.core.api import *
from airtest.core.error import *
from poco.exceptions import *
from tools import Config
from tools import PushApk2Devices
from tools import StartApp
from core import RunTestCase
import sys

_print = print
def print(*args, **kwargs):
    _print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), *args, **kwargs)

def Main(processNo,devices):
    starttime=time.time()
    print("进入",processNo,"进程,devicename=",devices)
    isconnect=""
    try:
        connect_device("Android:///" + devices)
        time.sleep(1)
        auto_setup(__file__)
        isconnect="Pass"
    except Exception as e:
        print(e)
        isconnect="Fail"
        print( "连接设备",devices,"失败")
    if isconnect=="Pass":
        try:
            print( "设备", devices, "开始安装apk")
            installResult=PushApk2Devices.PushApk2Devices(devices)
            if installResult == "Success":
                print(devices,"确定安装成功")
                StartApp.StartApp(devices)
                sleep(5)
                RunTestCase.RunTestCase(starttime, devices)
                print( devices,"完成测试")
        except Exception as e:
            print(e)
            print("安装失败，installResult=", installResult)


def main():
    configPath = "./config.ini"
    devicesList = Config.getValue(configPath, "deviceslist",)
    #devicesList = getdevices()
    print("测试开始")
    try:
        pool = multiprocessing.Pool(processes = len(devicesList))
        print("启动进程池")
        results = []
        for i in range(len(devicesList)):
            pool.apply_async(Main, (i,devicesList[i],))#根据设备列表去循环创建进程，对每个进程调用下面的Main方法。
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


# 本方法用于读取实时的设备连接
def getdevices():
    deviceslist=[]
    for devices in os.popen("adb devices"):
        if "\t" in devices:
            if devices.find("emulator")<0:
                deviceslist.append(devices.split("\t")[0])

    return deviceslist



