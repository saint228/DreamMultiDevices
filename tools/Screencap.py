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
    try:
        png= GetScreenbyMiniCap(starttime,devices,action)
    except:
        print("MiniCap截图失败，换ADB截图")
        png=GetScreenbyADBCap(starttime,devices,action)
    return  png

def GetScreenbyADBCap(starttime,devices,action):
    if ":" in devices:
        nickname = devices.split(":")[1]
    print("screenpath=",screenpath)
    png = screenpath +"\\"+ time.strftime('%Y%m%d_%H%M%S',time.localtime(starttime))+ nickname+ "_" + action+ ".png"
    print("png=",png)
    os.system(adb + " -s " + devices + " shell screencap -p /sdcard/screencap.png")
    time.sleep(1)
    fp = open(png, "a+", encoding="utf-8")
    fp.close()
    os.system(adb + " -s " + devices + " pull /sdcard/screencap.png " + png)
    time.sleep(0.5)
    compressImage(png)
    print("<img src='" + png + "' width=600 />")
    return png

def GetScreenbyMiniCap(starttime,devices,action):
    if ":" in devices:
        nickname = devices.split(":")[1]
    png = screenpath + "\\" + time.strftime("%Y%m%d_%H%M%S_", time.localtime(starttime)) + nickname + "_" + action + ".png"
    wmsizecommand = adb + " -s {} shell wm size".format(devices)
    size = os.popen(wmsizecommand).read()
    size = size.split(":")[1].strip()
    screen=adb  + " -s {} shell \" LD_LIBRARY_PATH=/data/local/tmp /data/local/tmp/minicap -P {}@{}/0 -s > /sdcard/screencap.png\"".format(devices,size, size)
    print(screen)
    result=os.popen(screen).read()
    #print(result)
    os.system(adb + " -s " + devices + " pull /sdcard/screencap.png " + png)
    print("<img src='" + png + "' width=600 />")
    print("返回的png为",png)
    return png

    # 图片压缩批处理
def compressImage(path,cr=0.2,left=0,right=1,top=0,buttom=1):
    # 打开原图片压缩
    sImg =Image.open(path)
    w, h = sImg.size# 获取屏幕绝对尺寸
    box=(int(w*left),int(h*top),int(w*right),int(h*buttom))
    sImg=sImg.crop(box)
    time.sleep(0.1)
    dImg = sImg.resize((int(w*cr), int(h*cr)), Image.ANTIALIAS)  # 设置压缩尺寸和选项
    time.sleep(0.1)
    # 压缩图片路径名称
    dImg.save(path)  # save这个函数后面可以加压缩编码选项JPEG之类的



if __name__=="__main__":
    #GetScreen(time.time(),"172.16.6.82:7437","test")
    GetScreenbyMiniCap(time.time(),"172.16.6.82:7597","test")


