# -*- coding: utf-8 -*-
__author__ = "无声"

from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from tools import Config
_print = print
def print(*args, **kwargs):
    _print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), *args, **kwargs)

def StartApp(devices):
    configPath = "../config.ini"
    packagename = Config.getValue(configPath, "packName")[0]
    start_app(packagename)

    # 获取andorid的poco代理对象，准备进行开启应用权限（例如申请文件存储、定位等权限）点击操作
    pocoAndroid = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
    if devices == "127.0.0.1:62001":
        #这里是针对不同机型进行不同控件的选取，需要用户根据自己的实际机型实际控件进行修改
        count=0
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