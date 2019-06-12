from DreamMultiDevices.start import *
from DreamMultiDevices.core.MultiAdb import MultiAdb as Madb
import multiprocessing
import time
import  threading
from DreamMultiDevices.tools.Excel import *

_print = print
def print(*args, **kwargs):
    _print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), *args, **kwargs)

def enter_performance(madb,timeout=3600):
    starttime=time.time()
    try:
        filepath, sheet, wb = create_log_excel(time.localtime(), madb.get_nickname())
        while True:
            if time.time()-starttime>timeout:
                break
            total=allocated= used=free=totalcpu= allocatedcpu=""
            getallocatedmemory = MyThread(madb.get_allocated_memory,args=())
            getmemoryinfo = MyThread(madb.get_memoryinfo,args=())
            gettotalcpu = MyThread(madb.get_totalcpu,args=() )
            getallocatedcpu = MyThread(madb.get_allocated_cpu,args=() )

            getallocatedmemory.start()
            getmemoryinfo.start()
            gettotalcpu.start()
            getallocatedcpu.start()

            allocated=getallocatedmemory.get_result()
            total,free,used=getmemoryinfo.get_result()
            totalcpu,maxcpu=gettotalcpu.get_result()
            allocatedcpu=getallocatedcpu.get_result()

            getallocatedmemory.join()
            getmemoryinfo.join()
            gettotalcpu.join()
            getallocatedcpu.join()
            if maxcpu=="":
                maxcpu="100%"

            nowtime = time.localtime()
            inputtime = time.strftime("%H:%M:%S", nowtime)
            list = [inputtime, total, allocated, used, free, totalcpu+"/"+maxcpu, allocatedcpu]
            record_to_excel(sheet, list)
        wb.save()
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
        except Exception:
            return None

if __name__ == "__main__":
    devicesList = Madb().getdevices()
    pool = multiprocessing.Pool(processes=len(devicesList))
    print("启动进程池")
    results = []
    for i in range(len(devicesList)):
        madb = Madb(devicesList[i])
        pool.apply_async(enter_performance, (madb,))  # 根据设备列表去循环创建进程，对每个进程调用下面的enter_processing方法。
    pool.close()
    pool.join()
    print("性能测试结束")