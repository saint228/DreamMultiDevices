# -*- coding: utf-8 -*-
__author__ = "无声"

import traceback
import os,inspect
import time
from PIL import Image
from airtest.core.android.adb import ADB


_print = print
def print(*args, **kwargs):
    _print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), *args, **kwargs)

adb = ADB().adb_path
parentPath = os.path.abspath(os.path.dirname(inspect.getfile(inspect.currentframe())) + os.path.sep + ".")
rootPath = os.path.abspath(os.path.dirname(parentPath) + os.path.sep + ".")
reportpath = os.path.join(rootPath, "Report")
screenpath = os.path.join(reportpath, "Screen")

def  GetScreen(starttime,devices,action):
    ABIcommand = adb + " -s {} shell getprop ro.product.cpu.abi".format(devices)
    ABI = os.popen(ABIcommand).read().strip()
    if ABI=="x86":
        png = GetScreenbyADBCap(starttime, devices, action)
    else:
        try:
            png= GetScreenbyMiniCap(starttime,devices,action)
        except:
            print("MiniCap截图失败，换ADB截图")
            png=GetScreenbyADBCap(starttime,devices,action)
    return  png

#用ADBCAP的方法截图
def GetScreenbyADBCap(starttime,devices,action):
    #先给昵称赋值，防止生成图片的命名格式问题。
    if ":" in devices:
        nickname = devices.split(":")[1]
    else:
        nickname=devices
    print("screenpath=",screenpath)
    png = screenpath +"\\"+ time.strftime('%Y%m%d_%H%M%S',time.localtime(starttime))+ nickname+ "_" + action+ ".png"
    print("png=",png)
    os.system(adb + " -s " + devices + " shell screencap -p /sdcard/screencap.png")
    time.sleep(1)
    fp = open(png, "a+", encoding="utf-8")
    fp.close()
    os.system(adb + " -s " + devices + " pull /sdcard/screencap.png " + png)
    time.sleep(0.5)
    #ADB截图过大，需要压缩，默认压缩比为0.2，全屏。
    compressImage(png)
    print("<img src='" + png + "' width=600 />")
    return png

#用MiniCap的方法截图，使用前需要确保手机上已经安装MiniCap和MiniCap.so。一般用过STF和airtestide的手机会自动安装，若未安装，则可以执行Init_MiniCap.py，手动安装。
def GetScreenbyMiniCap(starttime,devices,action):
    # 先给昵称赋值，防止生成图片的命名格式问题。
    if ":" in devices:
        nickname = devices.split(":")[1]
    else:
        nickname=devices
    #创建图片
    png = screenpath + "\\" + time.strftime("%Y%m%d_%H%M%S_", time.localtime(starttime)) + nickname + "_" + action + ".png"
    #获取设备分辨率
    wmsizecommand = adb + " -s {} shell wm size".format(devices)
    size = os.popen(wmsizecommand).read()
    size = size.split(":")[1].strip()
    #将设备号和分辨率填入minicap的命令，获得截图。
    screen=adb  + " -s {} shell \" LD_LIBRARY_PATH=/data/local/tmp /data/local/tmp/minicap -P {}@{}/0 -s > /sdcard/screencap.png\"".format(devices,size, size)
    print(screen)
    os.popen(screen)
    time.sleep(0.5)
    os.system(adb + " -s " + devices + " pull /sdcard/screencap.png " + png)
    print("<img src='" + png + "' width=600 />")
    print("返回的png为",png)
    return png

    # 图片压缩批处理，cr为压缩比，其他参数为屏幕截取范围
def compressImage(path,cr=0.2,left=0,right=1,top=0,buttom=1):
    # 打开原图片压缩
    sImg =Image.open(path)
    w, h = sImg.size# 获取屏幕绝对尺寸
    box=(int(w*left),int(h*top),int(w*right),int(h*buttom))
    sImg=sImg.crop(box)
    time.sleep(0.1)
    # 设置压缩尺寸和选项
    dImg = sImg.resize((int(w*cr), int(h*cr)), Image.ANTIALIAS)
    time.sleep(0.1)
    # 压缩图片路径名称
    dImg.save(path)  # save这个函数后面可以加压缩编码选项JPEG之类的



if __name__=="__main__":
    #GetScreen(time.time(),"172.16.6.82:7437","test")
    GetScreenbyMiniCap(time.time(),"172.16.6.82:7597","test")


