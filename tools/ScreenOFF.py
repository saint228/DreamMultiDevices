__author__ = "无声"

# !/usr/bin/python
# -*- coding: UTF-8 -*-

import sys,os,time

def setScreenOFF(device):
    platform = sys.platform
    command1 = command2 = ""
    # setScreenON(device)
    if platform == "win32":
        command1 = "adb -s {}  shell dumpsys window policy|findstr mScreenOnFully".format(device)
    else:
        command1 = "adb -s {}  shell dumpsys window policy|grep mScreenOnFully".format(device)
    print(command1)
    result = os.popen(command1)
    line = result.read()
    if "mScreenOnEarly=false" in line:
        pass
    else:
        command2 = "adb -s {}  shell input keyevent 26".format(device)
        os.popen(command2)
    off = True
    n = 0
    while off or n < 10:
        result = os.popen(command1)
        line = result.read()
        if "mScreenOnEarly=true" in line:
            os.popen(command2)
            time.sleep(2)
        else:
            break
        n += 1
    print(device, "has been ScreenOFF")