# -*- coding: utf-8 -*-
__author__ = "无声"

import os
import sys
import threading
from core import RunTestCase

from tools import Config

from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

_print = print
def print(*args, **kwargs):
    _print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), *args, **kwargs)


class MultiAdb():

    def __init__(self):
        self.configPath = "./config.ini"
        self.devicesList = Config.getValue(self.configPath, "deviceslist", )
        self.apkpath = Config.getValue(self.configPath, "apkpath")[0]
        self.packagename = Config.getValue(self.configPath, "packName")[0]
        self.needclickinstall = Config.getValue(self.configPath, "needclickinstall")[0]
        self.needclickstartapp = Config.getValue(self.configPath, "needclickstartapp")[0]
        self.starttime=time.time()
        #snapshot("d:\\temp.png")


    # 本方法用于读取实时的设备连接
    def getdevices(self):
        deviceslist=[]
        for devices in os.popen("adb devices"):
            print("adb devices:{}".format(devices))
            if "\t" in devices:
                if devices.find("emulator")<0:
                    if devices.split("\t")[1] == "device\n":
                        deviceslist.append(devices.split("\t")[0])
                        print("设备{}被添加到deviceslist中".format(deviceslist))
        print("返回的devicelist为{}".format(deviceslist))
        return deviceslist

    def enter_processing(self,processNo,devices):
        print("进入{}进程,devicename={}".format(processNo,devices))
        isconnect=""
        try:
            connect_device("Android:///" + devices)
            time.sleep(1)
            auto_setup(__file__)
            isconnect="Pass"
            print("设备{}连接成功".format(devices))
            if isconnect == "Pass":
                try:
                    print("设备{}开始安装apk".format(devices))
                    needclickinstall = self.needclickinstall
                    needclickstartapp = self.needclickstartapp
                    installResult = self.PushApk2Devices(devices, needclickinstall)
                    if installResult == "Success":
                        print("{}确定安装成功".format(devices))
                        self.StartApp(devices, needclickstartapp)
                        time.sleep(5)
                        RunTestCase.RunTestCase(self.starttime, devices)
                        print("{}完成测试".format(devices))
                except Exception as e:
                    print(e)
                    print("{}安装/运行失败，installResult={}".format(devices, installResult))
            else:
                print("设备{}连接失败".format(devices))
        except Exception as e:
            print(e)
            isconnect="Fail"
            print( "连接设备{}失败".format(devices))
        return isconnect


    def StartApp(self,devices,needclickstartapp):
        print("{}进入StartAPP函数".format(devices))
        start_app(self.packagename)
        if needclickstartapp=="True":
            print("设备{}，needclickstartapp为{}，开始初始化pocoui，处理应用权限".format(devices,needclickstartapp))
            # 获取andorid的poco代理对象，准备进行开启应用权限（例如申请文件存储、定位等权限）点击操作
            pocoAndroid = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
            if devices == "127.0.0.1:62001":
                # 这里是针对不同机型进行不同控件的选取，需要用户根据自己的实际机型实际控件进行修改
                count = 0
                while not pocoAndroid("android.view.View").exists():
                    print("{}开启应用的权限点击，循环第{}次".format(devices,count))
                    if count >= 3:
                        break
                    if pocoAndroid("com.android.packageinstaller:id/permission_allow_button").exists():
                        pocoAndroid("com.android.packageinstaller:id/permission_allow_button").oclick()
                    else:
                        time.sleep(3)
                        count += 1
            elif devices == "127.0.0.1:62025":
                count = 0
                while not pocoAndroid("android.view.View").exists():
                    print("{}开启应用的权限点击，循环第{}次".format(devices,count))
                    if count >= 3:
                        break
                    if pocoAndroid("android:id/button1").exists():
                        pocoAndroid("android:id/button1").click()
                    else:
                        time.sleep(3)
                        count += 1
        else:
            print("设备{}，needclickstartapp为{}，不做开启权限点击操作".format(devices,needclickstartapp))
        return None

    def PushApk2Devices(self,device,needclickinstall):
        try:
            installThread = threading.Thread(target=self.AppInstall, args=(device, self.apkpath, self.packagename,))
            installThread.start()
            if needclickinstall=="True":
                print("设备{}，needclickinstall为{}，开始进行安装点击权限操作".format(device,needclickinstall))
                inputThread = threading.Thread(target=self.InputEvent, args=(device,))
                inputThread.start()
                inputThread.join()
            else:
                print("设备{}，needclickinstall为{}，不进行安装点击权限操作".format(device,needclickinstall))
            installThread.join()
            return "Success"
        except Exception as e:
            return e
        pass

    def AppInstall(self,devices, apkpath, package):
        print("设备{}开始进行自动安装".format(devices))
        try:
            if self.isinstalled(devices, package):
                uninstallcommand = "adb -s " + str(devices) + " uninstall " + package
                print("正在{}上卸载{},卸载命令为：{}".format(devices, package, uninstallcommand))
                #print("卸载结果：", os.system(uninstallcommand))

            installcommand = "adb -s " + str(devices) + " install -r " + apkpath
            result=os.popen(installcommand)
            res = result.read()
            for line in res.splitlines():
                print("output={}".format(line))
            print("正在{}上安装{},安装命令为：{}".format(devices, package, installcommand))
            if self.isinstalled(devices, package):
                print("{}上安装成功，退出AppInstall线程".format(devices))
                return "Install Success"
        except Exception as e:
            print("{}上安装异常".format(devices)+e)
            return "Install Fail"

    def InputEvent(self,devices):
        print("设备{}开始进行自动处理权限".format(devices))
        # 获取andorid的poco代理对象，准备进行开启安装权限（例如各个品牌的自定义系统普遍要求的二次安装确认、vivo/oppo特别要求的输入手机账号密码等）的点击操作。
        pocoAndroid = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
        # 这里是针对不同机型进行不同控件的选取，需要用户根据自己的实际机型实际控件进行修改
        n = 3
        if devices == "2983aa37":
            count = 0
            # 找n次或找到对象以后跳出，否则等5秒重试。
            while True:
                print("{}安装应用的权限点击，循环第{}次".format(devices,count))
                if count >= n:
                    print("{}退出InputEvent线程".format(devices))
                    break
                if pocoAndroid("com.coloros.safecenter:id/et_login_passwd_edit").exists():
                    pocoAndroid("com.coloros.safecenter:id/et_login_passwd_edit").set_text("qatest2019")
                    time.sleep(2)
                    if pocoAndroid("android.widget.FrameLayout").offspring("android:id/buttonPanel").offspring("android:id/button1").exists():
                        pocoAndroid("android.widget.FrameLayout").offspring("android:id/buttonPanel").offspring(
                            "android:id/button1").click()
                    break
                else:
                    time.sleep(5)
                count += 1
        elif devices == "127.0.0.1:62025":
            count = 0
            while True:
                print("{}安装应用的权限点击，循环第{}次".format(devices,count))
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
        print("设备{}进入isinstalled方法，package={}".format(devices,package))
        for pkg in commandresult:
            if "package:" + package in pkg:
                print("在{}上发现已安装{}".format(devices,package))
                return True
        print("在{}上没找到包{}".format(devices,package))
        return False