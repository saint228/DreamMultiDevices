# -*- coding: utf-8 -*-
__author__ = "无声"

import time
from multiprocessing import Process,Value
from DreamMultiDevices.core.MultiAdb import MultiAdb as Madb
from airtest.core.error import *
from poco.exceptions import *
from airtest.core.api import *
from DreamMultiDevices.core import RunTestCase
from DreamMultiDevices.tools.Email import *
from DreamMultiDevices.tools.ScreenOFF import *
import traceback
from DreamMultiDevices.Performance import *

index_print = print
def print(*args, **kwargs):
    index_print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), *args, **kwargs)

'''
整个框架的主程序，根据配置表读取设备，并逐一为其分配功能测试进程和性能测试进程。
由于每个设备需要调用2个进程配合工作，所以使用Value进行进程间通信。Value会传递一个int值，默认为0，在功能进程结束时通知性能进程随之结束。
'''

def main():
    #默认去config.ini里读取期望参与测试的设备，若为空，则选择当前连接的所有状态为“device”的设备
    devicesList = Madb().get_devicesList()
    if devicesList[0] == "":
        devicesList = Madb().getdevices()
    print("最终的devicesList=",devicesList)
    if Madb().get_apkpath()=="" or Madb().get_packagename()=="":
        print("配置文件填写不全，packagename和apkpath是必填项")
        devicesList=None
    #读取是否需要同步性能测试的配置。
    skip_performance=Madb().get_skip_performance()
    skip_performance=True if skip_performance=="1" else False
    is_storaged_by_excel=Madb().get_storage_by_excel()
    is_storaged_by_excel=True if is_storaged_by_excel=="1" else False
    adb_log = Madb().get_adb_log()
    adb_log=True if adb_log=="1" else False
    reportpath = os.path.join(os.getcwd(), "Report")
    # 没有Report目录时自动创建
    if not os.path.exists(reportpath):
        os.mkdir(reportpath)
        os.mkdir(reportpath + "/Screen")
        os.mkdir(reportpath + "/Data")
        print(reportpath)
    print("测试开始")
    if devicesList:
        try:
            print("启动进程池")
            list=[]
            # 根据设备列表去循环创建进程，对每个进程调用下面的enter_processing/enter_enter_performance方法。
            for i in range(len(devicesList)):
                #start会被传递到2个进程函数里，作为区分最终产物html和excel的标志
                start=time.localtime()
                madb=Madb(devicesList[i])
                if madb.get_androidversion()<5:
                    print("设备{}的安卓版本低于5，不支持。".format(madb.get_mdevice()))
                    continue
                else:
                    #进程通信变量flag，默认为0，完成测试时修改为1。
                    flag = Value('i', 0)
                    fpsflag= Value('i',0)
                    if not skip_performance:
                        p1 = Process(target=enter_performance, args=(madb,flag,start,is_storaged_by_excel,adb_log))
                        list.append(p1)
                p2=Process(target=enter_processing, args=(i,madb,flag,start,))
                list.append(p2)
            for p in list:
                p.start()
            for p in list:
                p.join()
            print("进程回收完毕")
            print("测试结束")
            screenoff=Madb().get_screenoff()
            screenoff = True if screenoff == "1" else False
            if screenoff:
                for i in devicesList:
                    setScreenOFF(i)
                    print("设备{}已灭屏".format(i))
        except AirtestError as ae:
            print("Airtest发生错误" + traceback.format_exc())
        except PocoException as pe:
            print("Poco发生错误" + traceback.format_exc())
        except Exception as e:
            print("发生未知错误" +  traceback.format_exc())
    else:
        print("未找到设备，测试结束")
    mailtext="自动化测试完毕"
    '''
    try:
        sendemail(mailtext)
    except Exception as e:
        print("邮件发送失败"+  traceback.format_exc())
    '''
'''
功能进程模块
首先调用airtest库的方法进行设备连接并初始化，然后读取配表，进行应用的安装、启动、权限点击等操作。同步的操作会分由线程来完成。
确定启动应用成功以后，调用分配测试用例的RunTestCase函数。
在用例执行完毕以后，将Value置为1。
'''

def enter_processing(processNo,madb,flag,start):
    devices = madb.get_mdevice()
    print("进入{}进程,devicename={}".format(processNo,devices))
    isconnect=""
    try:
        #调用airtest的各个方法连接设备
        connect_device("Android:///" + devices)
        time.sleep(madb.get_timeout_of_per_action())
        auto_setup(__file__)
        isconnect="Pass"
        print("设备{}连接成功".format(devices))
        installflag=""
        startflag=""
        if isconnect == "Pass":
            try:
                print("设备{}开始安装apk".format(devices))
                #尝试推送apk到设备上
                installResult = madb.PushApk2Devices()
                if installResult == "Success":
                    print("{}确定安装成功".format(devices))
                    installflag = "Success"
                if installResult == "Skip":
                    print("{}设备跳过PushAPK2Device步骤".format(devices))
                    installflag="Success"
            except Exception as e:
                print("{}安装失败，installResult={}".format(devices, installResult)+ traceback.format_exc())
            if installflag=="Success":
                try:
                    #尝试启动应用
                    madb.StartApp()
                    startflag = "Success"
                except Exception as e:
                    print("运行失败"+traceback.format_exc())
            time.sleep(madb.get_timeout_of_per_action())
            #应用启动成功则开始运行用例
            if (startflag=="Success"):
                RunTestCase.RunTestCase(madb, start)
                print("{}完成测试".format(devices))
            else:
                print("{}未运行测试。".format(devices))
        else:
            print("设备{}连接失败".format(devices))
    except Exception as e:
        print( "连接设备{}失败".format(devices)+ traceback.format_exc())
    #无论结果如何，将flag置为1，通知Performance停止记录。
    flag.value = 1


if __name__ == "__main__":
    screenoff = Madb().get_screenoff()
    screenoff = True if screenoff == "1" else False
    devicesList = Madb().getdevices()
    if screenoff:
        for i in devicesList:
            setScreenOFF(i)
            print("设备{}已灭屏".format(i))







