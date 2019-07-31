# -*- coding: utf-8 -*-
__author__ = "无声"

import xlwings as xw
import os
import time
import json
import numpy as np


def create_log_json(nowtime,device):
    create_time = time.strftime("%m%d%H%M", nowtime)
    jsonfile = create_time + "_" + device + "_log.json"
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

def  record_to_json(jsonfilepath,list):
    for i in range(len(list)):
        if list[i] =="N/a":
            list[i] = "0"
    list[1]=float(list[1])
    list[2]=float(list[2])
    list[3]=float(list[3])
    list[4]=float(list[4])
    list[5]=float(list[5])*100
    list[6]=float(list[6].split("%")[0])
    list[7]=float(list[7])
    f = open(jsonfilepath, "r+")
    strdata=f.read()
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

def calculate_by_json(jsonfile):
    f = open(jsonfile, "r+")
    strdata=f.read()
    f.seek(0)
    dictdata=json.loads(strdata)
    Max_AllocatedMemory=max(dictdata["AllocatedMemory"])
    for i in range(len(dictdata["AllocatedMemory"])):
        if (dictdata["AllocatedMemory"][i-1]) == 0:
            dictdata["AllocatedMemory"].remove(dictdata["AllocatedMemory"][i-1])
        if (dictdata["AllocatedCPU"][i-1]) == 0:
            dictdata["AllocatedCPU"].remove(dictdata["AllocatedCPU"][i-1])
        if (dictdata["FPS"][i-1]) == 0:
            dictdata["FPS"].remove(dictdata["FPS"][i-1])
    Min_AllocatedMemory=min(dictdata["AllocatedMemory"])
    Avg_AllocatedMemory=format(np.average(dictdata["AllocatedMemory"]),".2f")
    Max_AllocatedCPU=max(dictdata["AllocatedCPU"])
    Min_AllocatedCPU=min(dictdata["AllocatedCPU"])
    Avg_AllocatedCPU=format(np.average(dictdata["AllocatedCPU"]),".2f")
    Max_FPS=max(dictdata["FPS"])
    Min_FPS=min(dictdata["FPS"])
    Avg_FPS=format(np.average(dictdata["FPS"]),".2f")
    dictdata["data_count"].append({"Max_AllocatedMemory": [Max_AllocatedMemory], "Min_AllocatedMemory": [Min_AllocatedMemory], "Avg_AllocatedMemory": [Avg_AllocatedMemory], "Max_AllocatedCPU": [str(Max_AllocatedCPU)+"%"], "Min_AllocatedCPU": [str(Min_AllocatedCPU)+"%"], "Avg_AllocatedCPU": [str(Avg_AllocatedCPU)+"%"], "Max_FPS": [Max_FPS], "Min_FPS": [Min_FPS], "Avg_FPS": [Avg_FPS]})
    strdata=json.dumps(dictdata)
    print("strdata=",strdata)
    f.write(strdata)
    f.close()

