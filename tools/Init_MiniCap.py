# -*- coding: utf-8 -*-
__author__ = "无声"


import os
import inspect
import time
from airtest.core.android.adb import ADB
import traceback
from DreamMultiDevices.core.MultiAdb import MultiAdb as Madb
from DreamMultiDevices.tools.Screencap import *

_print = print
def print(*args, **kwargs):
    _print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), *args, **kwargs)

adb = ADB().adb_path

#用来给设备初始化MiniCap的，介绍见 https://blog.csdn.net/saint_228/article/details/92142914
def ini_MiniCap(devices):
    try:
        parent_path = os.path.abspath(os.path.dirname(inspect.getfile(inspect.currentframe())) + os.path.sep + ".")
        root_path = os.path.abspath(os.path.dirname(parent_path) + os.path.sep + ".")
        ABIcommand=adb+" -s {} shell getprop ro.product.cpu.abi".format(devices)
        ABI=os.popen(ABIcommand).read().strip()
        AndroidVersion = os.popen(adb + " -s {} shell getprop ro.build.version.sdk".format(devices)).read().strip()
        airtest_minicap_path=os.path.abspath(os.path.dirname(root_path) + os.path.sep + ".")+"\\airtest\\core\\android\\static\\stf_libs"
        airtest_minicapso_path= os.path.abspath(os.path.dirname(root_path) + os.path.sep + ".")+"\\airtest\\core\\android\\static\\stf_libs\\minicap-shared\\aosp\\libs\\"+"android-{}\\{}\\minicap.so".format(AndroidVersion,ABI)
        push_minicap=adb + " -s {} push {}/{}/minicap".format(devices,airtest_minicap_path,ABI) +" /data/local/tmp/"
        push_minicapso = adb + " -s {} push {}".format(devices, airtest_minicapso_path) + " /data/local/tmp/"
        os.popen(push_minicap)
        os.popen(push_minicapso)
        chmod=adb+ " -s {} shell chmod 777 /data/local/tmp/*".format(devices)
        os.popen(chmod)
        wm_size_command=adb+" -s {} shell wm size".format(devices)
        vm_size=os.popen(wm_size_command).read()
        vm_size=vm_size.split(":")[1].strip()
        start_minicap=adb + " -s {} shell LD_LIBRARY_PATH=/data/local/tmp /data/local/tmp/minicap -P {}@{}/0 -t".format(devices,vm_size,vm_size)
        result=os.popen(start_minicap).read()
        print(result)
        print("设备{}上已经成功安装并开启了MiniCap。".format(devices))
    except Exception as e:
        print( e,traceback.format_exc())

if __name__=="__main__":
    devicesList = Madb().get_devicesList()
    if devicesList[0] == "":
        devicesList = Madb().getdevices()
    print("最终的devicesList=", devicesList)
    for device in devicesList:
        #ini_MiniCap(device)
        GetScreenbyMiniCap(time.time(),device,"测试")
