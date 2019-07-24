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
from collections import deque

_print = print
def print(*args, **kwargs):
    _print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), *args, **kwargs)

def enter_performance(madb,flag,start):
    print("设备{}进入enter_performance方法".format(madb.get_mdevice()))
    #创表
    filepath, sheet, wb = create_log_excel(time.localtime(), madb.get_nickname())
    #塞数据
    #flag = Value('i', 0)
    collect_data(madb,sheet,flag)
    #计算各平均值最大值最小值等并塞数据
    avglist,maxlist,minlist=calculate(sheet)
    record_to_excel(sheet,avglist,color=(230, 230 ,250))
    record_to_excel(sheet,maxlist,color=(193, 255, 193))
    record_to_excel(sheet,minlist,color=(240, 255 ,240))
    wb.save()
    nowtime = time.strftime("%H%M%S", start)
    reportpath = os.path.join(os.getcwd(), "Report")
    filename = reportpath+"\\"+madb.get_nickname() + "_" + str(nowtime)+".html"
    #filename = "D:\\Python3.7\\lib\\site-packages\\DreamMultiDevices\\Report\\7429_184046.html"
    print("要操作的文件名为：",filename)
    reportPlusPath = EditReport(filename,wb,avglist,maxlist,minlist)
    print("设备{}生成报告：{}完毕".format(madb.get_mdevice(),reportPlusPath))



#接受设备madb类对象、excel的sheet对象、共享内存flag、默认延时一小时
def collect_data(madb,sheet,flag,timeout=3600):
    starttime=time.time()
    dequelist = deque([])
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
            #为了避免重复场景不渲染导致的fps统计为0，fps取过去一秒内的最大值（约8次）。
            Threadlist=[]
            for i in range(8):
                get_fps = MyThread(madb.get_fps, args=())
                Threadlist.append(get_fps)



            #批量执行
            get_allocated_memory.start()
            get_memory_info.start()
            get_total_cpu.start()
            get_allocated_cpu.start()
            get_png.start()
            for p in Threadlist:
                p.start()
                fpstmp = p.get_result()
                if fpstmp=="N/a":
                    fpstmp=0
                if len(dequelist) < 9 :
                    dequelist.append(fpstmp)
                else:
                    dequelist.popleft()
                    dequelist.append(fpstmp)
                    print("dequelist=",dequelist)
            fps=max(dequelist)

            #批量获得结果
            allocated=get_allocated_memory.get_result()
            total,free,used=get_memory_info.get_result()
            totalcpu,maxcpu=get_total_cpu.get_result()
            allocatedcpu=get_allocated_cpu.get_result()
            png=get_png.get_result()

            #批量回收线程
            get_allocated_memory.join()
            get_memory_info.join()
            get_total_cpu.join()
            get_allocated_cpu.join()
            get_png.join()
            get_fps.join()
            for p in Threadlist:
                p.join()

            #对安卓7以下的设备，默认不区分cpu内核数，默认值改成100%
            if maxcpu=="":
                maxcpu="100%"
            #将性能数据填充到一个数组里，塞进excel

            nowtime = time.localtime()
            inputtime = str(time.strftime("%H:%M:%S", nowtime))
            #print(inputtime,type(inputtime))
            list = ["'"+inputtime, total, allocated, used, free, totalcpu+"/"+maxcpu, allocatedcpu,fps]
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


def EditReport(path, wb,avglist,maxlist,minlist):
    #取项目的绝对路径

    rootPath = os.path.abspath(os.path.dirname(inspect.getfile(inspect.currentframe())) + os.path.sep + ".")
    templatePath= os.path.join(rootPath, "template")
    # 读取报告文件
    f = open(path, "r+", encoding="UTF-8")
    fr = f.read()
    f.close()



    # 拼接CSS样式
    fr_prev, fr_next = GetHtmlContent(fr, "</style>", True, 1)
    css = open(templatePath+"\\app.css", "r+", encoding='UTF-8')
    css_str = css.read()
    css.close()
    fr = fr_prev + "\n" + css_str + "\n" + fr_next

    # 拼接头部按钮
    fr_prev, fr_next = GetHtmlContent(fr, "<div", False,3 )
    header = open(templatePath+"\\header.html", "r+", encoding='UTF-8')
    header_str = header.read()
    header.close()
    fr = fr_prev + "\n" + header_str + "\n" + fr_next

    # 添加功能测试标记
    fr_prev, fr_next = GetHtmlContent(fr, "class=", False, 8)
    fr = fr_prev + 'id="functionReport" ' + fr_next

    # 拼接页面主体
    fr_prev, fr_next = GetHtmlContent(fr, "<script", False, 1)
    performance = open(templatePath+"\\performance.html", "r+", encoding='UTF-8')
    performance_str = performance.read()
    performance.close()
    fr = fr_prev + "\n" + performance_str + "\n" + fr_next

    # 拼接JS脚本
    fr_prev, fr_next = GetHtmlContent(fr, "</body>", True, 1)
    highchartspath=templatePath+"\\highcharts.js"
    highcharts_str="<script src = "+highchartspath+" > </script >"
    print(highcharts_str)
    js = open(templatePath+"\\app.js", "r+", encoding='UTF-8')
    js_str = js.read()
    js.close()
    fr = fr_prev + "\n" + highcharts_str+"\n"+js_str + "\n" + fr_next

    # 嵌入性能测试结果
    sheet = wb.sheets("Sheet1")
    Time_series=get_json(sheet,"Time")
    TotalMemory=get_json(sheet,"TotalMemory(MB)")
    AllocatedMemory=get_json(sheet,"AllocatedMemory(MB)")
    UsedMemory=get_json(sheet,"UsedMemory(MB)")
    FreeMemory=get_json(sheet,"FreeMemory(MB)")
    TotalCPU=get_json(sheet,"TotalCPU")
    AllocatedCPU=get_json(sheet,"AllocatedCPU")
    FPS=get_json(sheet,"FPS")
    PNG=get_json(sheet,"PNGAddress")
    Max_AllocatedMemory=maxlist[2]
    Min_AllocatedMemory=minlist[2]
    Avg_AllocatedMemory=avglist[2]
    Max_AllocatedCPU=maxlist[6]
    Min_AllocatedCPU=minlist[6]
    Avg_AllocatedCPU=avglist[6]
    Max_FPS=maxlist[7]
    Min_FPS=minlist[7]
    Avg_FPS=avglist[7]

    data_series=Time_series+"\n"+"var TotalMemory="+TotalMemory +"\n"+"var AllocatedMemory="+AllocatedMemory+"\n"+"var UsedMemory="+UsedMemory+"\n"+"var FreeMemory="\
         +FreeMemory+"\n"+"var TotalCPU="+TotalCPU+"\n"+"var AllocatedCPU="+AllocatedCPU+"\n"+"var FPS="+FPS+"\n"+"var PNG="+PNG+"\n"
    data_count={"Max_AllocatedMemory":[Max_AllocatedMemory],"Min_AllocatedMemory":[Min_AllocatedMemory],"Avg_AllocatedMemory":[Avg_AllocatedMemory],"Max_AllocatedCPU":[Max_AllocatedCPU],"Min_AllocatedCPU":[Min_AllocatedCPU],"Avg_AllocatedCPU":[Avg_AllocatedCPU],"Max_FPS":[Max_FPS],"Min_FPS":[Min_FPS],"Avg_FPS":[Avg_FPS]}
    data_count="\n"+"var data_count="+json.dumps(data_count)
    fr_prev, fr_next = GetHtmlContent(fr, "// tag data", False, 1)
    fr= fr_prev+data_series+"\n"+data_count+"\n"+fr_next



    # 写入文件
    newPath = path.replace(".html", "_PLUS.html")
    f = open( newPath, "w", encoding="UTF-8")
    f.write(fr)
    f.close()



    return newPath

# 获取需要插入性能图表的节点
def GetHtmlContent(content, tag, reverse=False, round_num=1):
    fr_r_index = ""
    if reverse:
        fr_r_index = content.rfind(tag)
    else:
        fr_r_index = content.find(tag)
    for i in range(1, round_num):
        if reverse:
            fr_r_index = content.rfind(tag, 0, fr_r_index)
        else:
            fr_r_index = content.find(tag, fr_r_index + 1)
    fr_prev = content[0:fr_r_index]
    fr_next = content[fr_r_index:len(content)]
    return fr_prev, fr_next

#调试代码，单独执行的话，flag默认为1。
if __name__ == "__main__":
    devicesList = Madb().getdevices()
    print("最终的devicesList=",devicesList)

    start=time.localtime()
    '''
    madb = Madb(devicesList[0])
    flag = Value('i', 0)
    enter_performance (madb, flag, start,)
    '''
    print("启动进程池")
    flag = Value('i', 0)
    Processlist=[]
    for i in range(len(devicesList)):
        madb = Madb(devicesList[i])
        if madb.get_androidversion()<5:
            print("设备{}的安卓版本低于5，不支持。".format(madb.get_mdevice()))
            break
        print("{}开始进行性能测试".format(madb.get_mdevice()))
        # 根据设备列表去循环创建进程，对每个进程调用下面的enter_processing方法。
        p = Process(target=enter_performance, args=(madb, flag, start,))
        Processlist.append(p)
    for p in Processlist:
        p.start()
    for p in Processlist:
        p.join()


    print("性能测试结束")