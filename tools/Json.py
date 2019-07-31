# -*- coding: utf-8 -*-
__author__ = "无声"

import xlwings as xw
import os
import time
import json

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
    print("json=",jsonfilepath)
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
    print("strdata=",strdata)
    f.close()
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
    f = open(jsonfilepath, "w")
    f.write(strdata)
    f.close()

def calculate_by_json(jsonfile):
    print("enter calculate_by_json")
    avglist=[1234,123,653]
    maxlist=[5643,654,654]
    minlist=[589,65,321]
    f = open(jsonfile, "r")
    strdata=f.read()
    f.close()
    dictdata=json.loads(strdata)
    dictdata["data_count"].append({"Max_AllocatedMemory": [110.97], "Min_AllocatedMemory": [5.31], "Avg_AllocatedMemory": [81.78], "Max_AllocatedCPU": ["15.00%"], "Min_AllocatedCPU": ["4.00%"], "Avg_AllocatedCPU": ["6.00%"], "Max_FPS": [59.0], "Min_FPS": [30.0], "Avg_FPS": [31.68]})
    strdata=json.dumps(dictdata)
    print("strdata=",strdata)
    f = open(jsonfile, "w")
    f.write(strdata)
    f.close()

