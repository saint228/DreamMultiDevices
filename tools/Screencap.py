# -*- coding: utf-8 -*-
__author__ = "无声"

import glob
import os
import time
from PIL import Image,ImageGrab


_print = print
def print(*args, **kwargs):
    _print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), *args, **kwargs)

def GetScreen(startTime,devices,action):
    reportpath = os.path.join(os.getcwd(), "Report")
    screenpath = os.path.join(reportpath, "Screen")
    print("screenpath=",screenpath)
    png = screenpath +"\\"+ time.strftime('%Y%m%d_%H%M%S', time.localtime(startTime)) + "_" +  "_" + action+ ".png"
    print("png=",png)
    os.system("adb -s " + devices + " shell screencap -p /sdcard/screencap.png")
    fp = open(png, "a+", encoding="utf-8")
    fp.close()
    os.system("adb -s " + devices + " pull /sdcard/screencap.png " + png)
    time.sleep(1)
    compressImage(png)
    print("<img src='" + png + "' width=600 />")
    return png

    # 图片压缩批处理


def compressImage(path,cr=0.2,left=0,right=1,top=0,buttom=1):
    # 打开原图片压缩
    sImg =Image.open(path)
    w, h = sImg.size# 获取屏幕绝对尺寸
    box=(int(w*left),int(h*top),int(w*right),int(h*buttom))
    sImg=sImg.crop(box)
    dImg = sImg.resize((int(w*cr), int(h*cr)), Image.ANTIALIAS)  # 设置压缩尺寸和选项
    # 压缩图片路径名称
    dImg.save(path)  # save这个函数后面可以加压缩编码选项JPEG之类的

if __name__=="__main__":
    #GetScreen(time.time(),"172.16.6.82:7437","test")
    pass


