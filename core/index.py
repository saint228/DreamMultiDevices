# -*- coding: utf-8 -*-
__author__ = "无声"

import time
from multiprocessing import Process, Pipe
from DreamMultiDevices.core.MultiAdb import MultiAdb as Madb
from airtest.core.error import *
from poco.exceptions import *
from airtest.core.api import *
from DreamMultiDevices.core import RunTestCase
import traceback
from DreamMultiDevices.Performance import *
import queue


_print = print
def print(*args, **kwargs):
    _print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), *args, **kwargs)

def main():
 
    devicesList = Madb().get_devicesList()
    if devicesList[0] == "":
        devicesList = Madb().getdevices()
    print("最终的devicesList=",devicesList)
    print("测试开始")
    if devicesList:
        try:
            print("启动进程池")
            list=[]
            for i in range(len(devicesList)):
                madb=Madb(devicesList[i])
                # 根据设备列表去循环创建进程，对每个进程调用下面的enter_processing/enter_enter_performance方法。
                if madb.get_androidversion()<5:
                    print("设备{}的安卓版本低于5，不支持。".format(madb.get_mdevice()))
                    continue
                else:
                    p1 = Process(target=enter_performance, args=(madb,))
                    list.append(p1)
                p2=Process(target=enter_processing, args=(i,madb,))
                list.append(p2)
            for p in list:
                p.start()
            for p in list:
                p.join()
            print("进程回收完毕")
            print("测试结束")
        except AirtestError as ae:
            print("Airtest发生错误" + traceback.format_exc())
        except PocoException as pe:
            print("Poco发生错误" + traceback.format_exc())
        except Exception as e:
            print("发生未知错误" +  traceback.format_exc())
    else:
        print("未找到设备，测试结束")

def enter_processing(processNo,madb):
    filepath=os.getcwd() +"\\"+ madb.get_nickname() + '.tmp'
    file = open(filepath, 'w')
    file.close()
    devices = madb.get_mdevice()
    print("进入{}进程,devicename={}".format(processNo,devices))
    isconnect=""
    try:
        connect_device("Android:///" + devices)
        time.sleep(madb.get_timeoutaction())
        auto_setup(__file__)
        isconnect="Pass"
        print("设备{}连接成功".format(devices))
        if isconnect == "Pass":
            try:
                print("设备{}开始安装apk".format(devices))
                installResult = madb.PushApk2Devices()
                if installResult == "Success":
                    print("{}确定安装成功".format(devices))
            except Exception as e:
                print("{}安装失败，installResult={}".format(devices, installResult)+ traceback.format_exc())
            try:
                madb.StartApp()
            except Exception as e:
                print("运行失败"+traceback.format_exc())
            time.sleep(madb.get_timeoutaction())
            RunTestCase.RunTestCase(madb)
            print("{}完成测试".format(devices))
        else:
            print("设备{}连接失败".format(devices))
    except Exception as e:
        isconnect="Fail"
        print( "连接设备{}失败".format(devices)+ traceback.format_exc())
    os.remove(filepath)
    return isconnect




