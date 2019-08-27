# -*- coding: utf-8 -*-
__author__ = "无声"

import xlwings as xw
import os
import time
import json
import numpy as np

'''
生成一个json文件用来存储每次性能测试的数据
'''

reportpath = os.path.join(os.getcwd(), "Report")
datapath=os.path.join(reportpath, "Data")

def create_log_json(nowtime,device):
    create_time = time.strftime("%m%d%H%M", nowtime)
    jsonfile =datapath+"\\"+ create_time + "_" + device + "_log.json"
    if os.path.exists(jsonfile):
        raise Exception( "FileHasExisted")
    f = open(jsonfile, "w")
    resultData = {
        "Time_series": [],
        "TotalMemory": [],
        "AllocatedMemory": [],
        "UsedMemory": [],
        "FreeMemory": [],
        "TotalCPU": [],
        "AllocatedCPU": [],
        "FPS": [],
        "PNGAddress": [],
        "data_count": [],
    }
    f.write(json.dumps(resultData))
    f.close()
    return jsonfile
'''
由于highcharts绘图需要浮点数，在记录到json前，先强制将所有的性能数据格式化一下。
'''
def  record_to_json(jsonfilepath,list):
    for i in range(len(list)):
        if list[i] =="N/a":
            list[i] = "0"
    list[1]=float(list[1])
    list[2]=float(list[2])
    list[3]=float(list[3])
    list[4]=float(list[4])
    list[5]=float(list[5])
    list[6]=float(list[6])
    list[7]=float(list[7])
    f = open(jsonfilepath, "r+")
    strdata=f.read()
    #将文件输入点定位到文件头，每次用最新数据覆盖老数据。
    f.seek(0)
    dictdata=json.loads(strdata)
    dictdata["Time_series"].append(list[0])
    dictdata["TotalMemory"].append(list[1])
    dictdata["AllocatedMemory"].append(list[2])
    dictdata["UsedMemory"].append(list[3])
    dictdata["FreeMemory"].append(list[4])
    dictdata["TotalCPU"].append(list[5])
    dictdata["AllocatedCPU"].append(list[6])
    dictdata["FPS"].append(list[7])
    dictdata["PNGAddress"].append(list[8])
    strdata=json.dumps(dictdata)
    f.write(strdata)
    f.close()

'''
类似excel的统计函数，计算各个字段的最大、最小、平均值。然后写回文件。
'''
def calculate_by_json(jsonfile):
    f = open(jsonfile, "r+")
    strdata=f.read()
    f.seek(0)
    dictdata=json.loads(strdata)
    memorylist=list(dictdata["AllocatedMemory"])
    cpulist=list(dictdata["AllocatedCPU"])
    fpslist=list(dictdata["FPS"])
    while 0 in memorylist:
        memorylist.remove(0)
    while 0 in cpulist:
        cpulist.remove(0)
    while 0 in fpslist:
        fpslist.remove(0)
    Max_AllocatedMemory=max(memorylist)
    Min_AllocatedMemory=min(memorylist)
    Avg_AllocatedMemory=format(np.average(memorylist),".2f")
    Max_AllocatedCPU=max(cpulist)
    Min_AllocatedCPU=min(cpulist)
    Avg_AllocatedCPU=format(np.average(cpulist),".2f")
    Max_FPS=Min_FPS=Avg_FPS="N/a"
    #防止对某些应用或某些机型，因取不到fps导致max函数报错因而中断流程的问题。
    if len(fpslist)!=0:
        Max_FPS=max(fpslist)
        Min_FPS=min(fpslist)
        Avg_FPS=format(np.average(fpslist),".2f")
    dictdata["data_count"].append({"Max_AllocatedMemory": [Max_AllocatedMemory], "Min_AllocatedMemory": [Min_AllocatedMemory], "Avg_AllocatedMemory": [Avg_AllocatedMemory], "Max_AllocatedCPU": [str(Max_AllocatedCPU)+"%"], "Min_AllocatedCPU": [str(Min_AllocatedCPU)+"%"], "Avg_AllocatedCPU": [str(Avg_AllocatedCPU)+"%"], "Max_FPS": [Max_FPS], "Min_FPS": [Min_FPS], "Avg_FPS": [Avg_FPS]})
    strdata=json.dumps(dictdata)
    print("strdata=",strdata)
    f.write(strdata)
    f.close()

