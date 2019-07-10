# -*- coding: utf-8 -*-
__author__ = "无声"

from DreamMultiDevices.start import *
from DreamMultiDevices.core.MultiAdb import MultiAdb as Madb
import time
import  threading
import  multiprocessing
import traceback
from DreamMultiDevices.tools.Excel import *
from DreamMultiDevices.tools.Screencap import *
from multiprocessing import Process,Value
import json


_print = print
def print(*args, **kwargs):
    _print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), *args, **kwargs)

def enter_performance(madb,flag,start):
    print("设备{}进入enter_performance方法".format(madb.get_mdevice()))
    #创表
    filepath, sheet, wb = create_log_excel(time.localtime(), madb.get_nickname())
    #塞数据
    collect_data(madb,sheet,flag)
    #计算各平均值最大值最小值等并塞数据
    avglist,maxlist,minlist=calculate(sheet)
    record_to_excel(sheet,avglist,color=(230, 230 ,250))
    record_to_excel(sheet,maxlist,color=(193, 255, 193))
    record_to_excel(sheet,minlist,color=(240, 255 ,240))
    wb.save()
    nowtime = time.strftime("%H%M%S", start)
    filename = madb.get_rootPath()+"\\Report\\"+madb.get_nickname() + "_" + str(nowtime)+".html"
    print("要操作的文件名为：",filename)
    print(get_json(sheet,"Time"),get_json(sheet,"FreeMemory(MB)"))



#接受设备madb类对象、excel的sheet对象、共享内存flag、默认延时一小时
def collect_data(madb,sheet,flag,timeout=3600):
    starttime=time.time()
    n=0
    try:
        while True:
            #当执行一小时或flag为1时，跳出。
            # Performance.py可以单独执行，检查apk的性能，此时要把下面的flag.value注掉。因为这个是用于进程通信的，单独执行性能时没有必要。
            n+=1
            #为了确保截取统计数据不出错，至少打印3行
            if (time.time() - starttime > timeout) or (flag.value==1 and n>3):
                break
            total=allocated= used=free=totalcpu= allocatedcpu=""

            #开启n个线程，每个线程去调用Madb类里的方法，获取adb的性能数据
            get_allocated_memory = MyThread(madb.get_allocated_memory,args=())
            get_memory_info = MyThread(madb.get_memoryinfo,args=())
            get_total_cpu = MyThread(madb.get_totalcpu,args=() )
            get_allocated_cpu = MyThread(madb.get_allocated_cpu,args=() )
            get_png=MyThread(GetScreen,args=(time.time(), madb.get_mdevice(), "performance"))
            get_fps = MyThread(madb.get_fps, args=())
            #批量执行
            get_allocated_memory.start()
            get_memory_info.start()
            get_total_cpu.start()
            get_allocated_cpu.start()
            get_png.start()
            get_fps.start()
            #批量获得结果
            allocated=get_allocated_memory.get_result()
            total,free,used=get_memory_info.get_result()
            totalcpu,maxcpu=get_total_cpu.get_result()
            allocatedcpu=get_allocated_cpu.get_result()
            png=get_png.get_result()
            fps,jank_count=get_fps.get_result()
            #批量回收线程
            get_allocated_memory.join()
            get_memory_info.join()
            get_total_cpu.join()
            get_allocated_cpu.join()
            get_png.join()
            get_fps.join()
            #对安卓7以下的设备，默认不区分cpu内核数，默认值改成100%
            if maxcpu=="":
                maxcpu="100%"
            #将性能数据填充到一个数组里，塞进excel

            nowtime = time.localtime()
            inputtime = str(time.strftime("%H:%M:%S", nowtime))
            #print(inputtime,type(inputtime))
            list = ["'"+inputtime, total, allocated, used, free, totalcpu+"/"+maxcpu, allocatedcpu,fps,jank_count]
            record_to_excel(sheet,list,png=png)

    except Exception as e:
        print(madb.get_mdevice()+ traceback.format_exc())

#线程类，用来获取线程函数的返回值
class MyThread(threading.Thread):
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        threading.Thread.join(self)  # 等待线程执行完毕
        try:
            return self.result
        except Exception as e:
            print( traceback.format_exc())
            return None

#调试代码，单独执行的话，flag默认为1。
if __name__ == "__main__":
    devicesList = Madb().getdevices()
    pool = multiprocessing.Pool(processes=len(devicesList))
    print("启动进程池")
    for i in range(len(devicesList)):
        madb = Madb(devicesList[i])
        flag = Value('i', 1)
        if madb.get_androidversion()<5:
            print("设备{}的安卓版本低于5，不支持。".format(madb.get_mdevice()))
            break
        pool.apply_async(enter_performance, (madb,flag))  # 根据设备列表去循环创建进程，对每个进程调用下面的enter_processing方法。
    pool.close()
    pool.join()
    print("性能测试结束")