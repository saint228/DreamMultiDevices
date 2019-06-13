# -*- coding: utf-8 -*-
__author__ = "无声"

from DreamMultiDevices.start import *
from DreamMultiDevices.core.MultiAdb import MultiAdb as Madb
import time
import  threading
import  multiprocessing
from DreamMultiDevices.tools.Excel import *
from DreamMultiDevices.tools.Screencap import *

_print = print
def print(*args, **kwargs):
    _print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), *args, **kwargs)

def enter_performance(madb):
    print("设备{}进入enter_performance方法".format(madb.get_mdevice()))
    filepath, sheet, wb = create_log_excel(time.localtime(), madb.get_nickname())
    collect_data(madb,sheet)
    avglist=calculate_avg(sheet)
    maxlist=calculate_max(sheet)
    minlist=calculate_min(sheet)
    record_to_excel(sheet,avglist,color=(230, 230 ,250))
    record_to_excel(sheet,maxlist,color=(193, 255, 193))
    record_to_excel(sheet,minlist,color=(240, 255 ,240))

def calculate_avg(sheet):
    avglist=["合计："]
    return avglist

def calculate_max(sheet):
    maxlist=["最大值："]
    return maxlist
def calculate_min(sheet):
    minlist=["最小值："]
    return minlist


def collect_data(madb,sheet,timeout=3600):
    starttime=time.time()
    file=os.getcwd()+"\\"+madb.get_nickname()+".tmp"
    print("collect_data",file)
    try:

        while True:
            if (time.time()-starttime>timeout)or not os.path.exists(file):
                break
            total=allocated= used=free=totalcpu= allocatedcpu=""

            get_allocated_memory = MyThread(madb.get_allocated_memory,args=())
            get_memory_info = MyThread(madb.get_memoryinfo,args=())
            get_total_cpu = MyThread(madb.get_totalcpu,args=() )
            get_allocated_cpu = MyThread(madb.get_allocated_cpu,args=() )
            get_png=MyThread(GetScreen,args=(time.time(), madb.get_mdevice(), "performance"))

            get_allocated_memory.start()
            get_memory_info.start()
            get_total_cpu.start()
            get_allocated_cpu.start()
            get_png.start()
            
            allocated=get_allocated_memory.get_result()
            total,free,used=get_memory_info.get_result()
            totalcpu,maxcpu=get_total_cpu.get_result()
            allocatedcpu=get_allocated_cpu.get_result()
            time.sleep(1)
            png=get_png.get_result()

            get_allocated_memory.join()
            get_memory_info.join()
            get_total_cpu.join()
            get_allocated_cpu.join()
            get_png.join()

            if maxcpu=="":
                maxcpu="100%"

            nowtime = time.localtime()
            inputtime = str(time.strftime("%H:%M:%S", nowtime))
            list = [inputtime, total, allocated, used, free, totalcpu+"/"+maxcpu, allocatedcpu]

            record_to_excel(sheet,list,png=png)

    except Exception as e:
        print(madb.get_mdevice(),e)


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
            print(e)
            return None

if __name__ == "__main__":
    devicesList = Madb().getdevices()
    pool = multiprocessing.Pool(processes=len(devicesList))
    print("启动进程池")
    for i in range(len(devicesList)):
        madb = Madb(devicesList[i])
        if madb.get_androidversion()<5:
            break
        pool.apply_async(enter_performance, (madb,))  # 根据设备列表去循环创建进程，对每个进程调用下面的enter_processing方法。
    pool.close()
    pool.join()
    print("性能测试结束")