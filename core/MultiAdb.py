# -*- coding: utf-8 -*-
__author__ = "无声"

import os
import sys
import threading
import multiprocessing
from airtest.core.error import *
from poco.exceptions import *
from tools import Config
from core import RunTestCase
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

_print = print
def print(*args, **kwargs):
    _print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), *args, **kwargs)


class MultiAdb():

    def __init__(self):
        self.configPath = "./config.ini"
        self.devicesList = Config.getValue(self.configPath, "deviceslist", )

    def connectdevices(self):
        devicesList=self.devicesList
        if devicesList[0] == "":
            devicesList = self.getdevices()
        print("测试开始")
        try:
            pool = multiprocessing.Pool(processes=len(devicesList))
            print("启动进程池")
            results = []
            for i in range(len(devicesList)):
                pool.apply_async(self.enter_processing, (i, devicesList[i],))  # 根据设备列表去循环创建进程，对每个进程调用下面的Main方法。
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
    def getdevices(self):
        deviceslist=[]
        for devices in os.popen("adb devices"):
            if "\t" in devices:
                if devices.find("emulator")<0:
                    deviceslist.append(devices.split("\t")[0])
        return deviceslist

    def enter_processing(self,processNo,devices):
        starttime=time.time()
        print("进入{}进程,devicename={}".format(processNo,devices))
        isconnect=""
        try:
            connect_device("Android:///" + devices)
            time.sleep(1)
            auto_setup(__file__)
            isconnect="Pass"
        except Exception as e:
            print(e)
            isconnect="Fail"
            print( "连接设备{}失败".format(devices))
        if isconnect=="Pass":
            try:
                print( "设备{}开始安装apk".format(devices))
                installResult=self.PushApk2Devices(devices)
                if installResult == "Success":
                    print("{}确定安装成功".format(devices))
                    self.StartApp(devices)
                    sleep(5)
                    RunTestCase.RunTestCase(starttime, devices)
                    print( "{}完成测试".format(devices))
            except Exception as e:
                print(e)
                print("{}安装/运行失败，installResult={}".format(devices,installResult))

    def StartApp(self,devices):
        print("{}进入StartAPP函数".format(devices))
        configPath = "../config.ini"
        packagename = Config.getValue(configPath, "packName")[0]
        start_app(packagename)
        print("{}开始初始化pocoui，处理应用权限".format(devices))
        # 获取andorid的poco代理对象，准备进行开启应用权限（例如申请文件存储、定位等权限）点击操作
        pocoAndroid = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
        if devices == "127.0.0.1:62001":
            # 这里是针对不同机型进行不同控件的选取，需要用户根据自己的实际机型实际控件进行修改
            count = 0
            while not pocoAndroid("android.view.View").exists():
                print(devices, "开启应用的权限点击，循环第", count, "次")
                if count >= 3:
                    break
                if pocoAndroid("com.android.packageinstaller:id/permission_allow_button").exists():
                    pocoAndroid("com.android.packageinstaller:id/permission_allow_button").click()
                else:
                    time.sleep(3)
                    count += 1
        elif devices == "127.0.0.1:62025":
            count = 0
            while not pocoAndroid("android.view.View").exists():
                print(devices, "开启应用的权限点击，循环第", count, "次")
                if count >= 3:
                    break
                if pocoAndroid("android:id/button1").exists():
                    pocoAndroid("android:id/button1").click()
                else:
                    time.sleep(3)
                    count += 1

        return None

    def PushApk2Devices(self,devicesname):
        configPath = "./config.ini"
        packagename = Config.getValue(configPath, "packName")[0]
        apkpath = Config.getValue(configPath, "apkpath")[0]
        try:
            installThread = threading.Thread(target=self.AppInstall, args=(devicesname, apkpath, packagename,))
            inputThread = threading.Thread(target=self.InputEvent, args=(devicesname,))
            installThread.start()
            inputThread.start()
            installThread.join()
            inputThread.join()
            return "Success"
        except Exception as e:
            return e
        pass

    def AppInstall(self,devices, apkpath, package):
        try:
            if self.isinstalled(devices, package):
                uninstallcommand = "adb -s " + str(devices) + " uninstall " + package
                print("正在{}上卸载{},卸载命令为：{}".format(devices, package, uninstallcommand))
                print("卸载结果：", os.system(uninstallcommand))

            installcommand = "adb -s " + str(devices) + " install -r " + apkpath
            os.popen(installcommand).read()
            print("正在{}上安装{},安装命令为：{}".format(devices, package, installcommand))
            if self.isinstalled(devices, package):
                return "Install Success"
        except Exception as e:
            return "Install Fail"

    def InputEvent(self,devices):
        # 获取andorid的poco代理对象，准备进行开启安装权限（例如各个品牌的自定义系统普遍要求的二次安装确认、vivo/oppo特别要求的输入手机账号密码等）的点击操作。
        pocoAndroid = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
        # 这里是针对不同机型进行不同控件的选取，需要用户根据自己的实际机型实际控件进行修改
        n = 1
        if devices == "127.0.0.1:62001":
            count = 0
            # 找n次或找到对象以后跳出，否则等5秒重试。
            while True:
                print(devices, "安装点击，循环第", count, "次")
                if count >= n:
                    break
                if pocoAndroid("vivo:id/vivo_adb_install_ok_button").exists():
                    pocoAndroid("vivo:id/vivo_adb_install_ok_button").click()
                    break
                else:
                    time.sleep(5)
                count += 1
        elif devices == "127.0.0.1:62025":
            count = 0
            while True:
                print(devices, "安装点击，循环第", count, "次")
                if count >= n:
                    break
                if pocoAndroid("com.android.packageinstaller:id/continue_button").exists():
                    pocoAndroid("com.android.packageinstaller:id/continue_button").click()
                else:
                    time.sleep(5)
                count += 1

    def isinstalled(self,devices, package):
        command = "adb -s " + devices + " shell pm list packages"
        commandresult = os.popen(command)
        print("进入isinstalled方法，devices=", devices, "package=", package)
        for pkg in commandresult:
            if "package:" + package in pkg:
                print("在", devices, "上发现已安装：", package, "。")
                return True
        print("在", devices, "上没找到包：", package)
        return False